import json
import sys
import os
import logging
import random
import string
import torch
import experiment_utils as utils

sys.path.append(os.getcwd())
from dataset_creation.kb_crawl.utils.comet_transformers import CometAtomicModel
from dataset_creation import pre_processing_utils as proc

def run_pipeline(model, tokenizer, data_loader, possible_chars, sentences, number_of_trials, logger):
    
    dataset = proc.prepare_truism_data_for_sentence_scoring_comet(sentences,
                                                            possible_chars,
                                                            tokenizer,
                                                            data_loader,
                                                            number_of_trials)

    logger.info("finished creating dataset")

    perf = utils.generative_truism_reasoning_test(dataset, model, torch.cuda.is_available(), logger)

    logger.info("finished evaluating dataset")
    
    output_df = utils.convert_bi_statistic_results_into_df(perf)

    return output_df

def main():
    random.seed(1012)
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt = '%m/%d/%Y %H:%M:%S',
                        level = logging.INFO)
    logger = logging.getLogger(__name__)
    chars = list(string.ascii_uppercase.replace("A", "").replace("I", "").replace("U", ""))
    number_of_trials = 10

    comet_model = CometAtomicModel()

    tokenizer = comet_model.text_encoder
    data_loader = comet_model.data_loader
    model = comet_model.model

    # with open("data/generation_test_data/physical_data_sentences.json", "r") as f:
    #     physical_sents = json.load(f)

    # logger.info("finished reading in physical data")

    # output_df = run_pipeline(model=model,
    #                          tokenizer=tokenizer,
    #                          data_loader=data_loader,
    #                          possible_chars=chars, 
    #                          sentences=physical_sents, 
    #                          number_of_trials=number_of_trials,
    #                          logger=logger)

    # output_df.to_csv("data/generation_result_data/comet_atomic/physical_perf_{}.csv".format(number_of_trials),
    #                  index=False)

    # logger.info("finished saving physical dataset results")

        
    # with open("data/generation_test_data/material_data_sentences.json", "r") as f:
    #     material_sents = json.load(f)
        

    # logger.info("finished reading in material data")

    # output_df = run_pipeline(model=model,
    #                          tokenizer=tokenizer,
    #                          data_loader=data_loader,
    #                          possible_chars=chars, 
    #                          sentences=material_sents, 
    #                          number_of_trials=number_of_trials,
    #                          logger=logger)

    # output_df.to_csv("data/generation_result_data/comet_atomic/material_perf_{}.csv".format(number_of_trials),
    #                  index=False)

    # logger.info("finished saving material dataset results")
        
    # with open("data/generation_test_data/social_data_sentences.json", "r") as f:
    #     social_sents = json.load(f)

    # logger.info("finished reading in social data")

    # output_df = run_pipeline(model=model,
    #                          tokenizer=tokenizer,
    #                          data_loader=data_loader,
    #                          possible_chars=chars, 
    #                          sentences=social_sents, 
    #                          number_of_trials=number_of_trials,
    #                          logger=logger)

    # output_df.to_csv("data/generation_result_data/comet_atomic/social_perf_{}.csv".format(number_of_trials),
    #                  index=False)

    # logger.info("finished saving social dataset results")

    with open("data/generation_test_data/temporal_data_sentences.json", "r") as f:
        temporal_sents = json.load(f)

    logger.info("finished reading in temporal data")

    output_df = run_pipeline(model=model,
                             tokenizer=tokenizer,
                             data_loader=data_loader,
                             possible_chars=chars, 
                             sentences=temporal_sents, 
                             number_of_trials=number_of_trials,
                             logger=logger)

    output_df.to_csv("data/generation_result_data/comet_atomic/temporal_perf_{}.csv".format(number_of_trials),
                     index=False)

    logger.info("finished saving temporal dataset results")

if __name__ == "__main__":
    main()
