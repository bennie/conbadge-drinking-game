#!/usr/bin/perl -I/home/httpd/code/lib

use Anthrocon::SQL;
use Anthrocon::Time;
use strict;

my $as = new Anthrocon::SQL;
my $at = new Anthrocon::Time;

my $conyear = $at->con_year();

my %animals;

$animals{badger}    = [ qr/badger/i ];
$animals{bat}       = [ qr/bat/i ];
$animals{bear}      = [ qr/bear/i ];
$animals{bird}      = [ qr/bird/i, qr/crow/i, qr/raven/i ];
$animals{cat}       = [ qr/[ckq]at/i, qr/kitten/i, qr/kitty/i, qr/tabbie/i ];
$animals{cheetah}   = [ qr/cheetah/i ];
$animals{chipmunk}  = [ qr/chipmunk/i ];
$animals{cougar}    = [ qr/couga?r/i ];
$animals{coyote}    = [ qr/([ck]o)?yote/i ];
$animals{deer}      = [ qr/deer/i ];
$animals{dog}       = [ qr/dog/i, qr/husky/i, qr/pup(py)?/i, qr/hound/i, qr/canine/i ];
$animals{dragon}    = [ qr/dragon/i ];
$animals{ferret}    = [ qr/ferret/i ];
$animals{fox}       = [ qr/fox/i, qr/fennec/i, qr/kitsune/i, qr/vulpin(e)?/i, qr/vulpe(s)?/i ];
$animals{gazelle}   = [ qr/gazelle/i ];
$animals{goat}      = [ qr/goat/i ];
$animals{gryphon}   = [ qr/gryphon/i ];
$animals{horse}     = [ qr/horse/i, qr/pon[iy]/i ];
$animals{hyena}     = [ qr/hyena/i ];
$animals{lion}      = [ qr/lion/i ];
$animals{lynx}      = [ qr/lynx/i ];
$animals{mouse}     = [ qr/mous(i)?e/i ];
$animals{otter}     = [ qr/otter/i ];
$animals{panther}   = [ qr/panther/i ];
$animals{rabbit}    = [ qr/rabbit/i, qr/bunny/i, qr/bunnie/i, qr/bunn\b/i ];
$animals{racoon}    = [ qr/(ra)?coon/i ];
$animals{rat}       = [ qr/rat/i ];
$animals{roo}       = [ qr/kangaroo/i, qr/roo\b/i ];
$animals{skunk}     = [ qr/skunk(ie)?/i ];
$animals{snake}     = [ qr/snake/i, qr/python/i ];
$animals{squirrel}  = [ qr/squirrel/i ];
$animals{tiger}     = [ qr/t[iy]g(re|e?r)/i, qr/tora/i ];
$animals{unicorn}   = [ qr/unicorn/i ];
$animals{weasel}    = [ qr/weasel/i ];
$animals{wolf}      = [ qr/w[ou]l[fv](i?e)?([ei]n)?(e?y)?/i, qr/lupin(e)?/i ];
$animals{woodchuck} = [ qr/woodchuck/i ];
$animals{zebra}     = [ qr/zebra/i ];

my %colors;
map {$colors{$_} = [ qr/$_/i ];} qw/black blue brown green red white yellow/;

my %metals;
map {$metals{$_} = [ qr/$_/i ];} qw/brass cobalt copper gold iron metal silver/;

my %seasons;
map {$seasons{$_} = [ qr/$_/i ];} qw/spring summer fall winter/;

my %elements;
map {$elements{$_} = [ qr/$_/i ];} qw/earth wind fire water/;

my %celestials;

$celestials{cloud}   = [ qr/cloud/i ];
$celestials{moon}    = [ qr/moon/i ];
$celestials{thunger} = [ qr/thunder/i ];
$celestials{sky}     = [ qr/\bsky/i ];
$celestials{shadow}  = [ qr/shadow/i ];
$celestials{shadow}  = [ qr/snow/i ];
$celestials{star}    = [ qr/star/i ];
$celestials{sun}     = [ qr/\bsun/i ];

## Assemble the tests

my %tests;

$tests{animal}    = \%animals;
$tests{color}     = \%colors;
$tests{metal}     = \%metals;
$tests{season}    = \%seasons;
$tests{element}   = \%elements;
$tests{celestial} = \%celestials;

# Load unique badge names

my @names = $as->query_column('select badge_name from reg where con_year=?',$conyear);
my %unique;
map {$unique{$_}++} @names;

@names = sort keys %unique;
%unique = ();

### Run the tests

my $drinks = 0;
my %matches;
my %scores;
my %parses;

for my $name (@names) {
  for my $category ( keys %tests ) {
    for my $type ( keys %{$tests{$category}} ) {
      for my $test (@{$tests{$category}{$type}}) {
        while ( $name =~ /($test)/g ) { 
          $drinks++;
          $matches{$category}{$type}{$name}++;
          $scores{$name}++;
          $parses{$name}{$1}++;
        }
      }
    }
  }
  #if ( not defined $scores{$name} ) { print "No Score: $name\n"; }
}

print "$drinks drinks.\n";

for my $category ( sort keys %matches ) {
  for my $type ( sort keys %{$matches{$category}} ) {
    print "$category -> $type -> \n";
    print join(", ", sort keys %{$matches{$category}{$type}});
    print "\n\n";
  }
}

## Best score?

my $best = 0;

for my $name ( keys %scores ) {
  $best = $scores{$name} if $scores{$name} > $best;
}

print "The best score is $best. The following names scored this:\n";

for my $name ( sort { lc($a) cmp lc($b) } keys %scores ) {
  next unless $scores{$name} == $best;
  print "\t$name\n";

  for my $parse ( keys %{$parses{$name}} ) {
    print "\t -> $parse\n";
  }
}
