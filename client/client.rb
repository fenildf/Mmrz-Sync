#!/usr/bin/env ruby
# encoding = utf-8

require 'net/http'
require 'json'

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

# s = open("E:/Git_Mine/Mmrz/vocnw/word-ori.mmz", "rb").read

uri = URI('http://127.0.0.1:2603')
# uri = URI.parse 'http://zhanglin.work:2603'


# get demo
a = Net::HTTP.get(uri)
p a


# post demo
params = {}
params["word_rows"] = ["张麟", "咖啡"].to_json
res = Net::HTTP.post_form(uri, params)
puts res.body

