class TestDAGValidation:
    def test_import_dags(self, dagbag):
        assert len(dagbag.import_errors) == 0, f'DAG import failures. Errors: {dagbag.import_errors}'

    def test_alert_email_present(self, dagbag):
        for dag_id, dag in dagbag.dags.items():
            emails = dag.default_args.get('email', [])

            assert len(emails) > 0, f'Alert email not set for DAG {dag_id}'