#!/usr/bin/env ruby
# encoding = utf-8
require 'net/http'

Net::HTTP.start('127.0.0.1', 2603) do |http|
  response = http.get('/')
  head_hash = response.to_hash
  head_hash.keys.each do |key|
      puts key.to_s + ': ' + head_hash[key].to_s
  end

  puts response.body
end

