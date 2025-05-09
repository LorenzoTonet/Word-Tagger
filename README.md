## Word Tagger

This is a lightweight and user-friendly application designed to streamline the process of building custom datasets for training language models on text labeling tasks.

The app allows users to easily import raw text data and annotate selected portions with custom labels, making it ideal for creating training data for Named Entity Recognition (NER), intent classification, or any other sequence labeling tasks. Its intuitive interface helps accelerate dataset creation without the need for complex tooling or manual formatting.

### Features
- Upload or paste raw text content  
- Select and tag text spans with custom labels  
- Export labeled data in a structured format  
- Supports multiple label types and annotation sessions  
- Designed for ease of use and quick prototyping  

### Output Format
Currently, the exported dataset is formatted specifically for compatibility with the [spaCy](https://spacy.io) library. The output structure follows the format expected by `spacy.training.Example` and other training utilities, making it easy to integrate into custom NLP pipelines.

This tool is especially useful for researchers, data scientists, and NLP practitioners preparing labeled corpora tailored to specific domain requirements.
