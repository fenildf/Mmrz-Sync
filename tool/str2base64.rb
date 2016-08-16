#!/env/bin/ruby
# encoding: utf-8

require 'sqlite3'
require 'base64'

class DBManager
  def initialize
    @db = SQLite3::Database.new "./USERS.db"
  end

  def exec command
    @db.execute command
  end
end

if ARGV == []
  puts "no parameters given"

elsif ARGV[0] == "view"
  dbm = DBManager.new
  rows = dbm.exec "select * from USERS"
  rows.each do |row|
    user = row[0]
    pass = row[1]
  end

  p rows

elsif ARGV[0] == "exec"
  dbm = DBManager.new
  rows = dbm.exec "select * from USERS"
  rows.each do |row|
    user = row[0]
    pass = row[1]
    base64_pass = Base64.strict_encode64 pass
    row[1] = base64_pass
  end

  rows.each do |row|
    dbm.exec "update USERS set username = '#{row[0]}', password = '#{row[1]}' where username = '#{row[0]}'"
  end

elsif ARGV[0] == "base64"
  if not ARGV[1]
    puts "no string given"
  else
    puts Base64.strict_encode64 ARGV[1]
  end

else
  puts "no case matched"
end


