#!/usr/bin/env nextflow

nextflow.enable.dsl=2

process nextquant{
    conda '/hpcnfs/techunits/bioinformatics/software/NextQuant/conda/'
    cpus params.threads
    maxRetries = 3
    memory { 15.GB * task.attempt }

    publishDir "${params.outdir}/${params.sample_name}", mode: 'copy'
    output:
        file("tmp/combined")
    
    script:
    """
        mkdir tmp
        cp ${params.raw_folder}/*raw tmp/
        currdir=`pwd`
        update_params.py -x ${params.xml} -t ${params.threads} -f ${params.fasta} -r \$currdir/tmp -o params.xml
        maxquant params.xml
    """
}


workflow{
    nextquant()
}
