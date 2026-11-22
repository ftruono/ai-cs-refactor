$pdflatex = 'pdflatex -shell-escape %O %S';

# --- pulizia completa con latexmk -C / -c ---
$bibtex_use = 2;
$clean_ext .= ' %R.brf %R.xmpdata %R.run.xml %R.synctex.gz _minted-%R/* _minted-%R';

# Dopo la pulizia di latexmk cancella anche i file generati nelle sottocartelle
# (.aux dei file inclusi con \include, pdfa.xmpi di pdfx), partendo dalla
# cartella del file .tex principale. Funziona su Windows, Linux e macOS.
use File::Find;
use File::Basename;
END {
    if ($cleanup_mode) {
        my %dirs = map { (dirname($_) => 1) } (@file_list ? @file_list : ('.'));
        find({ no_chdir => 1, wanted => sub {
            if (-f $_ && /\.(aux|xmpi)$/i) { unlink($_) and print "Latexmk: cancellato $_\n"; }
        }}, keys %dirs);
    }
}