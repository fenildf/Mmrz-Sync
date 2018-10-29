use 5.016;

my $cmd = "ps -ef | grep -v grep | grep phantom";
my @result = `$cmd`;

foreach (@result) {
    s/ +/ /g;
    s/^ //g;
    my @items = split(/ /, $_);
    my $pid = $items[1];
    `kill $pid`;
}


