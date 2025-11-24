import pandas as pd
import re
import os

class RubricLoader:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        
    def load(self):
        if not os.path.exists(self.excel_path):
            raise FileNotFoundError(f"File not found: {self.excel_path}")

        df_raw = pd.read_csv(self.excel_path, header=None) if self.excel_path.endswith('.csv') else pd.read_excel(self.excel_path, header=None)
        
        header_idx = self._find_header_row(df_raw)
        df = self._load_with_header(header_idx)
        col_map = self._map_columns(df)
        
        df[col_map['Category']] = df[col_map['Category']].ffill()
        df[col_map['Metric']] = df[col_map['Metric']].ffill()

        return self._parse_rubric_data(df, col_map)
    
    def _find_header_row(self, df_raw):
        for idx, row in df_raw.iterrows():
            row_str = str(row.values).lower()
            if "scoring creteria" in row_str or "score attributed" in row_str:
                return idx
        return 24
    
    def _load_with_header(self, header_idx):
        if self.excel_path.endswith('.csv'):
            return pd.read_csv(self.excel_path, header=header_idx)
        return pd.read_excel(self.excel_path, header=header_idx)
    
    def _map_columns(self, df):
        df.columns = [str(c).strip() for c in df.columns]
        col_map = {}
        for c in df.columns:
            cl = c.lower()
            if 'creteria' in cl and 'scoring' not in cl: 
                col_map['Category'] = c
            if 'metric' in cl: 
                col_map['Metric'] = c
            if 'scoring creteria' in cl: 
                col_map['Desc'] = c
            if 'key words' in cl: 
                col_map['Keywords'] = c
            if 'score attributed' in cl: 
                col_map['Points'] = c
            if 'total score' in cl:
                col_map['Total'] = c
        return col_map
    
    def _parse_rubric_data(self, df, col_map):
        rubric_data = []
        for _, row in df.iterrows():
            try:
                points = row.get(col_map['Points'])
                if pd.isna(points): 
                    continue
                
                item = {
                    "category": str(row[col_map['Category']]),
                    "metric": str(row[col_map['Metric']]),
                    "description": str(row[col_map['Desc']]),
                    "points": float(points),
                    "max_score": float(row.get(col_map.get('Total', 'Points'), points)),
                    "keywords": [],
                    "min_val": -float('inf'),
                    "max_val": float('inf'),
                    "has_range": False
                }

                kw_raw = str(row.get(col_map['Keywords'], ""))
                self._parse_keywords_or_ranges(kw_raw, item)
                rubric_data.append(item)
            except:
                continue
        return rubric_data
    
    def _parse_keywords_or_ranges(self, kw_raw, item):
        range_match = re.search(r'([\d\.]+)\s*(?:to|–|-)\s*([\d\.]+)', kw_raw)
        gte_match = re.search(r'>=\s*([\d\.]+)', kw_raw)
        gt_match = re.search(r'>\s*([\d\.]+)', kw_raw)
        lte_match = re.search(r'<=\s*([\d\.]+)', kw_raw)
        lt_match = re.search(r'<\s*([\d\.]+)', kw_raw)

        if range_match:
            item['min_val'] = float(range_match.group(1))
            item['max_val'] = float(range_match.group(2))
            item['has_range'] = True
        elif gte_match:
            item['min_val'] = float(gte_match.group(1))
            item['has_range'] = True
        elif gt_match:
            item['min_val'] = float(gt_match.group(1))
            item['has_range'] = True
        elif lte_match:
            item['max_val'] = float(lte_match.group(1))
            item['has_range'] = True
        elif lt_match:
            item['max_val'] = float(lt_match.group(1))
            item['has_range'] = True
        elif kw_raw and kw_raw.lower() != 'nan' and kw_raw.strip() != '-':
            clean_kw = kw_raw.replace('\n', ',')
            item['keywords'] = [k.strip() for k in clean_kw.split(',') if k.strip()]
