use strict;
use Getopt::Long;
my $infile;
my $rootdir;

GetOptions('in=s' => \$infile, 'out=s'=> \$rootdir ) or die "USAGE...";
$infile = "..\\..\\ExtShoots_testData - Sheet1.csv";
$rootdir = "..\\..\\Pictures\\images";
open(IN,$infile) or die "FAILED to open $infile";
my @inlines = <IN>;
#print "@inlines\n";
chomp @inlines;
foreach my $line (@inlines){
    my $classnum = $1;
    my $minnum = $2;
    my $maxnum = $3;
#    print "--- $line ---\n";
    $line =~ /^\d/ or next;    
    $line =~ /(\d+),(\d+)[,\s]+(\d+)/;
    $classnum = $1;
    $minnum = $2;
    $maxnum = $3;
    if(!defined($1)){
        $line =~ /(\d+),\s*(\d+)\s*/;
        $classnum = $1;
        $minnum = $2;
    } 
    my $dir = "$rootdir\\$classnum";
    if(!-e $dir){
        mkdir($dir) || die;
    }
    
    print "$line-- $classnum -- $minnum -- $maxnum -- \n";
}