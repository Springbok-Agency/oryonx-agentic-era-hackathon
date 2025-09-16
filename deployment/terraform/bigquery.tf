# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

resource "google_bigquery_dataset" "agent_telemetry" {
  for_each      = local.deploy_project_ids
  project       = each.value
  dataset_id    = "agent_telemetry"
  friendly_name = "Agent Telemetry"
  description   = "Dataset for storing agent telemetry data"
  location      = var.region
}

resource "google_bigquery_ml_model" "gemini_model" {
  for_each      = local.deploy_project_ids
  provider      = google-beta
  project       = each.value
  dataset_id    = google_bigquery_dataset.agent_telemetry[each.key].dataset_id
  model_id      = "gemini_model"
  friendly_name = "Gemini Pro"
  description   = "Gemini Pro model for generating insights from agent telemetry"
  model_type    = "CLOUD_AI_LARGE_LANGUAGE_MODEL"
  location      = var.region

  model_options {
    model_id = "gemini-pro"
  }
}
