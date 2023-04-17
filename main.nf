#!/usr/bin/env nextflow

nextflow.enable.dsl=2

process nextquant{
    conda '/hpcnfs/data/PGP/zhan/miniconda3/envs/nextquant'
    cpus 10
    memory "30 G"

    publishDir "results", mode: 'copy'
    output:
        file("combined/txt/*.txt")
    
    script:
    """
        update_params.py -x ${params.xml} -t ${params.threads} -f ${params.fasta} -r ${params.raw_folder} -o params.xml
        ## run MQ
        maxquant params.xml

    """
}


workflow{
    nextquant()
}