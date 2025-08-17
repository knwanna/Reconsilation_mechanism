// src/constants.js
export const LOCAL_STORAGE_KEY = 'reconciliation-services-state';

export const fileAccept = {
  'tabular': '.csv, .tsv, .xlsx',
  'image': 'image/*',
  'video': 'video/*',
  'audio': 'audio/*',
  'text': '.txt, .json, .xml, .yaml, .rdf, .ttl, .n3',
  '3d-model': '.obj, .mtl, .fbx',
  'gis': '.shp, .kml, .geojson', 
  'all-files': '*'
};


export const RECON_STATUS = {
  MATCHED: 'M',
  UNMATCHED: 'U',
  PENDING: 'P'
};
