# Data Licensing & Attribution

| Dataset | Source | License / Terms | Required Attribution |
|---------|--------|-----------------|----------------------|
| Kepler DR25 | NASA Exoplanet Archive (MAST) | NASA Open Data Portal; public domain but request acknowledgement | “Data products courtesy of the NASA Exoplanet Archive and missions funded by the NASA Science Mission Directorate.” |
| TESS Full Frame Images / Light curves | MAST (https://mast.stsci.edu) | Public domain; follow TESS mission acknowledgment | “This research makes use of data collected by the TESS mission, funded by NASA´s Science Mission Directorate.” |
| K2 Campaigns | NASA Kepler/K2 mission archive | Public domain | Same as Kepler acknowledgment |
| Synthetic augmentation assets | Generated with PyTransit/BATMAN | MIT (PyTransit) / MIT (batman-package) | Cite package manuals in technical appendix |
| NASA ADS Literature | NASA/ADS | Terms of Use allow indexing & citation with attribution | Provide DOI or canonical reference within evidence panel |

## Usage Guidelines
1. Preserve metadata (mission, sector, cadence) when persisting records in the SQL catalog to enable traceable provenance.
2. When redistributing pre-trained models or dashboards, include a “Data Sources” section referencing the table above.
3. For citizen science campaigns, display a footer notice: “NASA data are publicly available; analysis performed by ExoAI team.”
4. Synthetic data blends must not exceed 80% per release unless flagged as simulated in export metadata (`source_metadata.synthetic: true`).

## Citation Template
> “This project uses the NASA Exoplanet Archive, TESS mission data (Ricker et al. 2015), and supporting literature indexed via NASA ADS. Software libraries include PyTransit (Parviainen 2015) and batman (Kreidberg 2015).”
