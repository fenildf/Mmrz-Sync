/*
 * notie.js - A clean and simple notification plugin (alert/growl style) for javascript, with no dependencies.
 *
 * Copyright (c) 2015 Jared Reich
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 * https://jaredreich.com/projects/notie.js
 *
 * Version:  2.1.0
 *
*/

var notie = function(){

    // SETTINGS
    // *********************************************

    // General
    var shadow = true;
    var font_size_small = '15px';
    var font_size_big = '24px';
    var font_change_screen_width = 600;
    var animation_delay = 0.3;
    var background_click_dismiss = true;

    // notie.alert colors
    var alert_color_success_background = '#57BF57';
    var alert_color_warning_background = '#E3B771';
    var alert_color_error_background = '#E1715B';
    var alert_color_info_background = '#4D82D6';
    var alert_color_text = '#FFF';
    
    // ID's for use within your own .css file (OPTIONAL)
    // (Be sure to use !important to override the javascript)
    // Example: #notie-alert-inner { padding: 30px !important; }
    var alert_outer_id = 'notie-alert-outer';
    var alert_inner_id = 'notie-alert-inner';
    var alert_text_id = 'notie-alert-text';

    // HELPERS
    // *********************************************
    // Function for resize listeners for font-size
    var resizeListener = function resizeListener(ele) {
        ele.style.fontSize = font_size_small;
        // if (window.innerWidth <= font_change_screen_width) { ele.style.fontSize = font_size_small; }
        // else { ele.style.fontSize = font_size_big; }
    };

    // Debounce function (credit to Underscore.js)
    var debounce_time = 500;
    var debounce = function debounce(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    // Event listener for enter and escape keys
    window.addEventListener('keydown', function(event) {
        var enter_clicked = (event.which == 13 || event.keyCode == 13);
        var escape_clicked = (event.which == 27 || event.keyCode == 27);
        if (alert_is_showing) {
            if (enter_clicked || escape_clicked) {
                clearTimeout(alert_timeout_1);
                clearTimeout(alert_timeout_2);
                alert_hide();
            }
        }
    });

    // addEventListener polyfill, fixes a style.height issue for IE8
    if (typeof Element.prototype.addEventListener === 'undefined') {
        Element.prototype.addEventListener = Window.prototype.addEventListener = function (e, callback) {
            e = 'on' + e;
            return this.attachEvent(e, callback);
        };
    }

    // Scroll disable and enable for notie.confirm and notie.input
    var original_body_height, original_body_overflow;
    function scroll_disable() {
        original_body_height = document.body.style.height;
        original_body_overflow = document.body.style.overflow;
        document.body.style.height = '100%';
        document.body.style.overflow = 'hidden';
    }
    function scroll_enable() {
        document.body.style.height = original_body_height;
        document.body.style.overflow = original_body_overflow;
    }
    // *********************************************

    // NOTIE.ALERT
    // *********************************************

    // notie elements and styling
    var alert_outer = document.createElement('div');
    alert_outer.id = alert_outer_id;
    alert_outer.style.position = 'fixed';
    alert_outer.style.top = '0';
    alert_outer.style.left = '0';
    alert_outer.style.zIndex = '999999999';
    alert_outer.style.height = 'auto';
    alert_outer.style.width = '100%';
    alert_outer.style.display = 'none';
    alert_outer.style.textAlign = 'center';
    alert_outer.style.cursor = 'default';
    alert_outer.style.MozTransition = '';
    alert_outer.style.WebkitTransition = '';
    alert_outer.style.transition = '';
    alert_outer.style.cursor = 'pointer';

    // Hide alert on click
    alert_outer.onclick = function() {
        clearTimeout(alert_timeout_1);
        clearTimeout(alert_timeout_2);
        alert_hide();
    };

    var alert_inner = document.createElement('div');
    alert_inner.id = alert_inner_id;
    alert_inner.style.padding = '5px';
    alert_inner.style.display = 'table-cell';
    alert_inner.style.verticalAlign = 'middle';
    alert_outer.appendChild(alert_inner);

    // Initialize notie text
    var alert_text = document.createElement('span');
    alert_text.id = alert_text_id;
    alert_text.style.color = alert_color_text;
    alert_text.style.fontSize = font_size_small;
    // if (window.innerWidth <= font_change_screen_width) { alert_text.style.fontSize = font_size_small; }
    // else { alert_text.style.fontSize = font_size_big; }
    window.addEventListener('resize', debounce(resizeListener.bind(null, alert_text), debounce_time), true);
    alert_inner.appendChild(alert_text);

    // Attach notie to the body element
    $(document.body).append(alert_outer);

    // Declare variables
    var height = 0;
    var alert_is_showing = false;
    var alert_timeout_1;
    var alert_timeout_2;
    var was_clicked_counter = 0;

    function alert(type, message, seconds) {

        // Blur active element for use of enter key, focus input
        document.activeElement.blur();

        was_clicked_counter++;

        setTimeout(function() {
            was_clicked_counter--;
        }, (animation_delay * 1000 + 10));

        if (was_clicked_counter == 1) {

            if (alert_is_showing) {

                clearTimeout(alert_timeout_1);
                clearTimeout(alert_timeout_2);

                alert_hide(function() {
                    alert_show(type, message, seconds);
                });

            }
            else {
                alert_show(type, message, seconds);
            }

        }

    }

    function alert_show(type, message, seconds) {

        alert_is_showing = true;

        var duration = 0;
        if (typeof seconds == 'undefined') {
            var duration = 3000;
        }
        else if (seconds < 1) {
            duration = 1000;
        }
        else {
            duration = seconds * 1000;
        }

        // Set notie type (background color)
        switch(type) {
            case 1:
                alert_outer.style.backgroundColor = alert_color_success_background;
                break;
            case 2:
                alert_outer.style.backgroundColor = alert_color_warning_background;
                break;
            case 3:
                alert_outer.style.backgroundColor = alert_color_error_background;
                break;
            case 4:
                alert_outer.style.backgroundColor = alert_color_info_background;
                break;
        }

        // Set notie text
        alert_text.innerHTML = message;

        // Get notie's height
        alert_outer.style.top = '-10000px';
        alert_outer.style.display = 'table';
        alert_outer.style.top = '-' + alert_outer.offsetHeight - 5 + 'px';

        alert_timeout_1 = setTimeout(function() {

            if (shadow) { alert_outer.style.boxShadow = '0px 0px 10px 0px rgba(0,0,0,0.5)'; }
            alert_outer.style.MozTransition = 'all ' + animation_delay + 's ease';
            alert_outer.style.WebkitTransition = 'all ' + animation_delay + 's ease';
            alert_outer.style.transition = 'all ' + animation_delay + 's ease';

            alert_outer.style.top = 0;

            alert_timeout_2 = setTimeout(function() {

                alert_hide(function() {
                    // Nothing
                });
            }, duration);

        }, 20);
    }

    function alert_hide(callback) {

        alert_outer.style.top = '-' + alert_outer.offsetHeight - 5 + 'px';

        setTimeout(function() {

            if (shadow) { alert_outer.style.boxShadow = ''; }
            alert_outer.style.MozTransition = '';
            alert_outer.style.WebkitTransition = '';
            alert_outer.style.transition = '';
            
            alert_outer.style.top = '-10000px';

            alert_is_showing = false;

            if (callback) { callback(); }

        }, (animation_delay * 1000 + 10));
    }

    return {
        alert: alert
    };

}();

if (typeof module !== 'undefined' && module) {
    module.exports = notie;
}