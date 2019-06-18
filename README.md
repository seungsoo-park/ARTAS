## ARTAS
Automatic Research Trend Analysis System(ARTAS) is a for information security research trend analysis. Our system collects research papers in the field of information security, and extracts and analyzes key keywords. You can identify trends in information security research based on the analysis results.

### Functions of ARTAS
* Collecting Korean and international journal papers : Korea(KIISC) and International(ACM CCS, IEEE S&P, USENIX Security, NDSS).
* Major keyword extraction : Keyword extraction based on KOMORAN morpheme analyzer and Ahnlab security terminology dictionary.
Keyword relationship analysis : Generate graphs of relationships between keywords through network analysis.
* Our information security research trends service web page : http://hpsclab.hannam.ac.kr/artas/

### Advantages of ARTAS
* Automation system : our systems are all efficient because they run automatically.
* Very fast analysis speed : our system can collect and analyze data for 10 years within about 443 seconds per journal. This is much faster than manual analysis.
* Little performance overhead : since the average number of papers published in each journal is 420 per year, there is little performance overhead.
* Prediction of future research keywords(coming soon)

### Usege
We uploaded only the sample code. We will upload a full version with additional features in the future.

KIISC crawler will be uploaded after modification. This is because the web page where the data was collected has been modified.

Collect paper data:
```python
python ./data_crawler_module/semantic_scholar_crawler.py
```
Morpheme analysis: 
```python
python ./data_analysis_module/morpheme_analyzer.py
```
Network analysis:
```python 
python ./data_analysis_module/network_analyzer.py
```

The analysis results will be generated in the 'analyzed_data' directory.
