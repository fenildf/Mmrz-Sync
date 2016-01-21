#!/usr/bin/env ruby
# encoding = utf-8
require 'net/http'

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

require 'json'

s = open("E:/Git_Mine/Mmrz/vocnw/word-ori.mmz", "rb").read
puts "sending"

uri = URI('http://115.29.192.240:2603')
uri = URI.parse 'http://zhanglin.work:2603'
params = {}  
params["q"] = s 
res = Net::HTTP.post_form(uri, params)   
puts res.header['set-cookie']  
puts res.body

# http = Net::HTTP.new(uri.host, uri.port)
# req = Net::HTTP::Post.new(uri.request_uri)
# req.set_form_data("q"=>s)
# response = http.request(req)
# puts response.body
