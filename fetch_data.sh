#!/bin/bash
mkdir -p data
git clone https://github.com/JetBrains/kotlin.git
python3 prepare_kotlin_dataset.py
rm -rf kotlin