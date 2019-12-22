# Simple Image Search Engine
This is a simple image search engine using PIL and PyQt5 for an assignment in CPE651 (1/2019) class.

### Dataset
You can use any image which PIL supports, store them in one folder.

### How to use
1. Clone the repository.
2. Install required python3 libraries by running:
```
pip3 install -r simpleImageSearchEngine/requirements.txt
```
3. Create "index" folder inside the repository directory.
4. Run `python3 generate_index_dir.py` to generate an index (Use option `--imgDir` point to the image data set directory).
5. Once an index directory is created, you can either use a simple search script or one with GUI.
* If you want to use a script without GUI, run this following command:
```
python3 search_index_dir.py <image_file_path>
```
* Otherwise, you prefer to use a script with GUI, run this following command instead:
```
python3 simple_image_search_engine.py
```
