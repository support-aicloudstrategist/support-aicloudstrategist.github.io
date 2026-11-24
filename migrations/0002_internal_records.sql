CREATE TABLE IF NOT EXISTS internal_records (
  company TEXT NOT NULL,
  module TEXT NOT NULL,
  id TEXT NOT NULL,
  data TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  updated_by TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  PRIMARY KEY (company, module, id)
);
CREATE INDEX IF NOT EXISTS idx_internal_records_list ON internal_records(company, module, updated_at DESC);
