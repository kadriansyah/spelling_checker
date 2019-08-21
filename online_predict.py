import argparse
import os

from google.cloud import automl_v1beta1 as automl

#export PROJECT_ID="704499156902"
#export REGION_NAME="us-central1"
#export GOOGLE_APPLICATION_CREDENTIALS="/Users/kadriansyah/projects/personal/python/spelling_checker/development-234608-b4134bc85973.json"

def predict(project_id, compute_region, model_id, text):
	automl_client = automl.AutoMlClient()

	# Get the full path of the model.
	model_full_id = automl_client.model_path(project_id, compute_region, model_id)

	# Create client for prediction service.
	prediction_client = automl.PredictionServiceClient()

	values = []
	values.append({'string_value': text})
	payload = {
		'row': {'values': values}
	}

	# Query model
	response = prediction_client.predict(model_full_id, payload)
	print("Prediction results:")
	print(response.payload)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter,
	)
	subparsers = parser.add_subparsers(dest="command")

	predict_parser = subparsers.add_parser("predict", help=predict.__doc__)
	predict_parser.add_argument("--model_id")
	predict_parser.add_argument("--text")

	project_id = os.environ["PROJECT_ID"]
	compute_region = os.environ["REGION_NAME"]

	args = parser.parse_args()

	if args.command == "predict":
		predict(project_id, compute_region, args.model_id, args.text)