#!/usr/bin/env ruby
# encoding = utf-8

require 'net/http'
require 'json'
require 'base64'

require './db'

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

dbMgr = MmrzDBManager.new
rows_all = dbMgr.readAllDB

def urlencode params
  URI.escape(params.collect{|k, v| "#{k}=#{v}"}.join('&'))
end

def version_to_int ver
  ver.gsub!(/[^\d]/, "").to_i
end

# params = {
#   # 'req_thing' => 'occupied_client'
#   'req_thing' => 'version_info'
# }

# a = urlencode params
# uri = URI('http://127.0.0.1:2603/?' + a)
# # uri = URI.parse 'http://zhanglin.work:2603/?' + a


# # get demo
# # rec = JSON.parse Net::HTTP.get(uri)
# # p rec['version_info']['CLI']
# # p version_to_int rec['version_info']['CLI']

# post demo
params = {
  # 'req_thing' => 'occupied_client'
  # 'post_thing' => 'login_data'
}

a = urlencode params
uri = URI('http://127.0.0.1:2603/upload_wordbook/?' + a)
# login = { "username" => "zhanglin", "password" => Base64.encode64('zhanglin') }
database = {"username"=>"yanbin", "password"=>"yanbin", "data"=>rows_all.to_json}
res = Net::HTTP.post_form(uri, database)
puts res.body

