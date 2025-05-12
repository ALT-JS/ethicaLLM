# ethicaLLM

> Are LLMs complicated ethical dilemma analyzers?

Project Code Repository for Advanced LLM Agents Team JJAZ.

**ethicaLLM** is a benchmark and evaluation framework designed to assess the ethical reasoning capabilities of Large Language Models (LLMs). By leveraging a curated dataset of 196 real-world ethical dilemmas, expert analyses, and non-expert human responses, this project aims to evaluate how closely LLMs can emulate human-like ethical decision-making processes. The repository includes structured prompts, evaluation metrics, and tools for fine-tuning and benchmarking LLMs in ethical contexts.

## Repository Structure
`Georgia ESTA dataset.csv` contains 51 sets of ethical dilemma data we used for experiments.

`Online Ethics Center Dataset.csv` contains 145 sets of extra data we processed from the Internet.

`human_answers.csv` contains human answers from 4 different non-expert individuals of the Georgia dataset.
```
data/
|--benchmark/
|----Georgia ESTA dataset.csv
|----Online Ethics Center Dataset.csv
|----human_answers.csv
|--experiments_data/
|----(omitted) // Contains all data we used in the paper, you can generate them using the script we provided.
metrics/
|--Graph.ipynb // For visualization
|--choosing_metrics.ipynb // Metrics choosing in methods part 4.2
|--final_pipeline.ipynb // Contains our final pipeline from preprocessed data to final scores
|--generate_scores.ipynb // Used for generate scores per part in methods 4.2
|--metric_requirements.txt // code repository requirements.txt
|--metric_test.ipynb // Inversion loss for weights implementation in methods part 4.2
|--metrics.py // The metrics class we defined for final score calculation
prompts/
|--generate_organized_file.ipynb // structured output for human baseline
|--human_prompt.py // prompt for human baseline data preprocessing
|--temp_expert_prompt.py // prompt for expert opinion preprocessing
|--temp_prompt.py // prompt for LLM answers generation
test/
|--(omitted) // contains code files used for strctured LLM answer generation
```

## Getting started
#### Clone repository
```
git clone https://github.com/ALT-JS/ethicaLLM.git
cd ethicaLLM
```
#### Install dependencies
Ensure you have Python 3.8 or higher installed.
```
conda create -n ethicallm
conda activate ethicallm
pip install -r metrics/metric_requirements.txt
```
#### Run our demo
Open `metrics/final_pipeline.ipynb` to run all the final scores across 4 different LLMs.

Open `test/<model_name>.ipynb` to run data preprocessing on `<model_name>`.