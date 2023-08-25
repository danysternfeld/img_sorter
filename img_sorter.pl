use strict;
use Getopt::Long;
use File::Find;
use File::Copy;
my $infile;
my $rootdir;
my $move;
my $debug;
GetOptions('in=s' => \$infile, 'out=s'=> \$rootdir,'move' =>\$move , 'debug'=>\$debug) or die "USAGE...";
$infile = "..\\..\\ExtShoots_testData - Sheet1.csv";
$rootdir = "..\\..\\Pictures\\images";
open(IN,$infile) or die "FAILED to open $infile";
my @inlines = <IN>;
print "@inlines\n" if $debug;
chomp @inlines;
foreach my $line (@inlines){
    my $classnum = $1;
    my $minnum = $2;
    my $maxnum = $3;
    print "--- $line ---\n" if $debug;
    $line =~ /^\d/ or next;    
    $line =~ /(\d+),(\d+)[,\s]+(\d+)/;
    $classnum = $1;
    $minnum = $2;
    $maxnum = $3;
    if($minnum > $maxnum){
        ($minnum,$maxnum) = ($maxnum,$minnum);
    }
    if(!defined($1)){
        $line =~ /(\d+),\s*(\d+)\s*/;
        $classnum = $1;
        $minnum = $2;
        $maxnum = undef;
    } 

    my $dir = "$rootdir\\$classnum";
    if(!-e $dir){
        mkdir($dir) || die;
    }
    my @files = [];
    my @dirpath=$rootdir;


    print "$line-- $classnum -- $minnum -- $maxnum -- \n" if $debug;
    find(
        sub {
           /(\d+)\./;
           my $imgnum = $1;
           if(!defined($maxnum)){
             push @files,$File::Find::name if (-f $File::Find::name and ($imgnum == $minnum));   
           } else {
            push @files,$File::Find::name 
                if (-f $File::Find::name and ($imgnum >= $minnum) and ($imgnum <= $maxnum));
           }
      }, @dirpath);
      foreach my $file (@files){
        if(!$move){
            copy($file,"$rootdir\\$dir");
        } else {
            move($file,"$rootdir\\$dir");
        }
      }

    print "@files\n" if $debug;

}







