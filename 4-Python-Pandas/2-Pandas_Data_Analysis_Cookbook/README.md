# Pandas Data Cleaning Portfolio Project

## 🧹 Professional Data Cleaning & Analysis Showcase

This repository demonstrates advanced **Pandas data cleaning techniques** using real-world datasets. The project showcases essential data preprocessing skills that are crucial for any data science workflow.

---

## 📊 Project Overview

This portfolio project focuses on comprehensive data cleaning and preparation techniques using two diverse datasets:
- **Climate Data**: Land temperature measurements from weather stations worldwide
- **Economic Data**: GDP per capita statistics by metropolitan areas

## 🎯 Learning Objectives & Skills Demonstrated

### Data Import & Configuration
- ✅ Advanced CSV reading with custom parameters
- ✅ Excel file processing with sheet selection and range specification
- ✅ Display option optimization for better data visualization

### Data Cleaning Techniques
- ✅ **Column Management**: Renaming, reordering, and selecting relevant columns
- ✅ **Data Type Conversion**: Converting object types to appropriate numeric formats
- ✅ **String Processing**: Handling leading/trailing whitespaces
- ✅ **Missing Data Handling**: Converting invalid entries to NaN values
- ✅ **Date Processing**: Parsing and combining date components

### Data Quality Assessment
- ✅ Data structure analysis using `.info()` and `.head()`
- ✅ Data type validation and conversion
- ✅ Missing value identification and handling

---

## 📁 Project Structure

```
├── README.md                          # Project documentation
├── Data_Cleaning_Portfolio.ipynb      # Main analysis notebook
└── data/                              # Raw datasets
    ├── landtempssample.csv            # Climate temperature data
    ├── GDPpercapita.xlsx              # Economic GDP data
    └── [other supporting files]
```

---

## 🗂️ Datasets Used

### 1. Land Temperature Dataset (`landtempssample.csv`)
- **Source**: Global weather station measurements
- **Features**: Station ID, coordinates, temperature, elevation, country information
- **Cleaning Focus**: Date parsing, column naming, data type optimization

### 2. GDP Per Capita Dataset (`GDPpercapita.xlsx`)
- **Source**: Economic statistics by metropolitan area
- **Features**: Metropolitan areas and GDP values from 2001-2018
- **Cleaning Focus**: Excel processing, string cleaning, numeric conversion

---

## 🔧 Technologies & Libraries

- **Python 3.x**
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations (implicit dependency)

---

## 🚀 Key Techniques Demonstrated

### 1. **Advanced Data Import**
```python
# CSV with custom parameters
landtemps = pd.read_csv('data/landtempssample.csv',
    names=['stationid','year','month','avgtemp','latitude',
      'longitude','elevation','station','countryid','country'],
    skiprows=1,
    parse_dates=[['month','year']],
    low_memory=False)

# Excel with specific sheet and range
percapitaGDP = pd.read_excel('data/GDPpercapita.xlsx', 
    sheet_name=1, skiprows=4, skipfooter=1, usecols="A, C:T")
```

### 2. **Data Type Optimization**
```python
# Convert multiple columns to numeric with error handling
for col in percapitaGDP.columns[1:]:
    percapitaGDP[col] = pd.to_numeric(percapitaGDP[col], errors='coerce')
```

### 3. **String Data Cleaning**
```python
# Remove leading and trailing whitespaces
percapitaGDP.metro_year = percapitaGDP.metro_year.str.strip()
```

---

## 📈 Results & Impact

This project demonstrates:
- **Clean, production-ready datasets** suitable for further analysis
- **Systematic approach** to data quality assessment
- **Reusable cleaning patterns** applicable to similar datasets
- **Professional data preprocessing** workflows

---

## 🎓 Skills Acquired

By completing this project, you'll master:
1. **Data Import Strategies** for various file formats
2. **Quality Assessment** techniques for raw data
3. **Systematic Cleaning** approaches for messy datasets
4. **Data Type Management** for optimal memory usage
5. **String Processing** for text data normalization

---

## 💻 How to Use

1. **Clone the repository**
2. **Install required dependencies**: `pip install pandas openpyxl`
3. **Open the Jupyter notebook**: `Data_Cleaning_Portfolio.ipynb`
4. **Run cells sequentially** to see the cleaning process
5. **Modify techniques** for your own datasets

---

## 🏆 Portfolio Highlights

This project showcases **professional-level data cleaning skills** essential for:
- Data Science roles
- Business Intelligence positions  
- Research analyst positions
- Any role requiring data preprocessing expertise

---

## 👤 Author

**Teslim Adeyanju**  
*Data Science Portfolio*

---

## 📧 Contact

Feel free to reach out for any questions about this project or collaboration opportunities!

---

*This project is part of my data science portfolio demonstrating practical pandas data cleaning skills with real-world applications.*