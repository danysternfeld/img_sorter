use strict;
use Getopt::Long;
use File::Find;
use File::Copy;
use Cwd;
my $infile;
my $rootdir;
my $move;
my $debug;
GetOptions('in=s' => \$infile, 'root=s'=> \$rootdir,'move' =>\$move , 'debug'=>\$debug) or die "USAGE...";
# testing...
#$infile = "..\\..\\ExtShoots_testData - Sheet1.csv";
#$rootdir = "..\\..\\Pictures\\images";
if(!defined($rootdir)){
    $rootdir = cwd();
}
if(!defined($infile)){
    my @files;
    my @dir;
    push(@dir,$rootdir);
    find(
        sub{
           push @files,$File::Find::name if (-f $File::Find::name &&  $File::Find::name =~/\.csv$/); 
           print "$File::Find::name" if $debug;
        },@dir
    );
    $infile = @files[0];
    print "infile = $infile\n" if $debug;
};
open(IN,$infile) or die "FAILED to open $infile";
my @inlines = <IN>;
print "@inlines\n" if $debug;
chomp @inlines;
foreach my $line (@inlines){
    # parse the csv
    # line can be a range in any order or single number 
    my $classnum = $1;
    my $minnum = $2;
    my $maxnum = $3;
    print "--- $line ---\n" if $debug;
    $line =~ /^\d/ or next;    
    $line =~ /(\d+),(\d+)[,\s]+(\d+)/;
    $classnum = $1;
    $minnum = $2;
    $maxnum = $3;
    # set the order right
    if($minnum > $maxnum){
        ($minnum,$maxnum) = ($maxnum,$minnum);
    }
    if(!defined($1)){
        $line =~ /(\d+),\s*(\d+)\s*/;
        $classnum = $1;
        $minnum = $2;
        $maxnum = undef;
    } 
    # set dest dir
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
            # just one number on the line - find file that matches
             push @files,$File::Find::name if (-f $File::Find::name and ($imgnum == $minnum));   
           } else {
            # find files in a range
            push @files,$File::Find::name 
                if (-f $File::Find::name and ($imgnum >= $minnum) and ($imgnum <= $maxnum));
           }
      }, @dirpath);
      foreach my $file (@files){
        # copy or move ( copy is dedfault)
        if(!$move){
            copy($file,"$rootdir\\$dir");
        } else {
            move($file,"$rootdir\\$dir");
        }
      }

    print "@files\n" if $debug;

}







