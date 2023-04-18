#!/usr/bin/env nextflow

nextflow.enable.dsl=2

process nextquant{
    conda '/hpcnfs/data/DIMA/zhan/NextQuant/maxquant.yml'
    cpus params.threads
    maxRetries = 3
    memory { 10.GB * task.attempt }

    publishDir "${params.outdir}/${params.sample_name}", mode: 'copy'
    output:
        file("txt/*.txt")
    
    script:
    """
        update_params.py -x ${params.xml} -t ${params.threads} -f ${params.fasta} -r ${params.raw_folder} -o params.xml
        ## run MQ
        export PATH=\$PATH:/usr/local/lib/dotnet/
        maxquant params.xml
        cp -r ${params.raw_folder}/combined/txt .
        rm -r ${params.raw_folder}/
    """
}


workflow{
    nextquant()
}