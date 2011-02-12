#!/usr/bin/perl

use CGI;
use CGI::Carp qw/fatalsToBrowser/;
use strict;

### Handle errors quickly

my $cgi = new CGI;
my $badgename = $cgi->param('badgename');

if ( $badgename ) {
  print $cgi->header;
} else {
  print $cgi->redirect('index.html');
  exit;
}

### TESTS

my %animals;

$animals{aquatic}   = [ qr/fish/i, qr/orca/i ];
$animals{badger}    = [ qr/badger/i ];
$animals{bat}       = [ qr/bat/i ];
$animals{bear}      = [ qr/bear/i, qr/panda/i ];
$animals{bird}      = [ qr/bird/i, qr/crow/i, qr/raven/i ];
$animals{buffalo}   = [ qr/buffalo/i ];
$animals{cat}       = [ qr/[ckq]at/i, qr/kitten/i, qr/kitty/i, qr/tabbie/i ];
$animals{cheetah}   = [ qr/cheetah/i ];
$animals{chipmunk}  = [ qr/chipmunk/i ];
$animals{cougar}    = [ qr/couga?r/i ];
$animals{coyote}    = [ qr/([ck]o)?yote/i ];
$animals{deer}      = [ qr/deer/i ];
$animals{dog}       = [ qr/can[iu]{0,2}s/i, qr/collie/i, qr/dog/i, qr/husky/i, qr/pup(py)?/i, qr/hound/i, qr/canine/i, qr/dingo/i ];
$animals{dragon}    = [ qr/dragon/i, qr/hydra/i, qr/wyvern/i ];
$animals{ferret}    = [ qr/ferret/i ];
$animals{fox}       = [ qr/fox/i, qr/fennec/i, qr/kitsune/i, qr/vixen/i, qr/vulpin(e)?/i, qr/vulpe(s)?/i ];
$animals{gazelle}   = [ qr/gazelle/i ];
$animals{goat}      = [ qr/goat/i ];
$animals{gryphon}   = [ qr/gryphon/i, qr/griff[io]n/i ];
$animals{horse}     = [ qr/horse/i, qr/pon[iy]/i ];
$animals{hyena}     = [ qr/hyena/i ];
$animals{jaguar}    = [ qr/jaguar/i ];
$animals{lion}      = [ qr/lion/i ];
$animals{lizard}    = [ qr/lizard/i ];
$animals{lynx}      = [ qr/lynx/i ];
$animals{mouse}     = [ qr/mous(i)?e/i ];
$animals{otter}     = [ qr/otter/i ];
$animals{panther}   = [ qr/panther/i ];
$animals{rabbit}    = [ qr/rabbit/i, qr/bunny/i, qr/bunnie/i, qr/bunn\b/i, qr/lapine/i ];
$animals{racoon}    = [ qr/(ra)?coon/i ];
$animals{rat}       = [ qr/rat/i ];
$animals{roo}       = [ qr/kangaroo/i, qr/roo\b/i ];
$animals{sheep}     = [ qr/sheep/i, qr/lamb/i ];
$animals{skunk}     = [ qr/skunk(ie)?/i ];
$animals{snake}     = [ qr/snake/i, qr/python/i ];
$animals{squirrel}  = [ qr/squirrel/i ];
$animals{tiger}     = [ qr/t[iy]g(re|e?r)/i, qr/tora/i ];
$animals{unicorn}   = [ qr/unicorn/i ];
$animals{weasel}    = [ qr/weasel/i, qr/mongoose/i ];
$animals{wolf}      = [ qr/(v|wh|w)+(0|o|ou|u|y)+(l*(f|ph|(?<!vol)v))+(ei?|ie|in|y)?/i, qr/lupin(e)?/i ];
$animals{woodchuck} = [ qr/woodchuck/i ];
$animals{zebra}     = [ qr/zebra/i ];

### Colors & metals

my %colors;
map {$colors{$_} = [ qr/$_/i ];} qw/black blue brown emerald green grey red white yellow/;

$colors{purple} = [ qr/pu?rple?/i ];

my %metals;
map {$metals{$_} = [ qr/$_/i ];} qw/brass cobalt copper gold iron metal silver/;

my %seasons;
map {$seasons{$_} = [ qr/$_/i ];} qw/spring summer fall winter/;

my %elements;
map {$elements{$_} = [ qr/$_/i ];} qw/earth wind fire flame water/;

my %celestials;

$celestials{angel}   = [ qr/angel/i ];
$celestials{anubis}  = [ qr/anubis/i ];
$celestials{demon}   = [ qr/demon/i ];
$celestials{god}     = [ qr/god/i ];

$celestials{moon}    = [ qr/moon/i ];
$celestials{thunder} = [ qr/thunder/i ];
$celestials{sky}     = [ qr/\bsky/i ];
$celestials{shadow}  = [ qr/shadow/i ];
$celestials{snow}    = [ qr/snow/i ];
$celestials{star}    = [ qr/star/i ];
$celestials{storm}   = [ qr/storm/i ];
$celestials{sun}     = [ qr/\bsun/i ];

my %opts;
$opts{wyld} = [ qr/wyld/i ];

## Assemble the tests

my %tests;

$tests{animal}    = \%animals;
$tests{color}     = \%colors;
$tests{metal}     = \%metals;
$tests{season}    = \%seasons;
$tests{element}   = \%elements;
$tests{celestial} = \%celestials;

$tests{opts}      = \%opts;

### Done with test

print $cgi->start_html;

my $drinks = 0;
my %matches;

for my $category ( keys %tests ) {
  for my $type ( keys %{$tests{$category}} ) {
    for my $test (@{$tests{$category}{$type}}) {
      while ( $badgename =~ /($test)/g ) { 
        $drinks++;
        $matches{$category}{$type}{$1}++;
      }
    }
  }
}

print $cgi->p("$badgename is worth $drinks drinks.");

for my $category ( sort keys %matches ) {
  for my $type ( sort keys %{$matches{$category}} ) {
    for my $match ( sort keys %{$matches{$category}{$type}} ) {
      print $cgi->p("$category -> $type -> \"$match\" is worth a drink!");
    }
  }
}

print $cgi->end_html;
