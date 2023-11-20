# Now defining the parameters.
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


cancer_model = BayesianNetwork([
    ('Pollution', 'Cancer'),
    ('Smoker', 'Cancer'),
    ('Cancer', 'XRay'),
    ('Cancer', 'Dyspnoea')
])
cpd_poll = TabularCPD(variable='Pollution', variable_card=2, values=[
                      [0.1], [0.9]], state_names={'Pollution': ['High', 'Low']})
cpd_smoke = TabularCPD(variable='Smoker', variable_card=2, values=[
                       [0.3], [0.7]], state_names={'Smoker': ['True', 'False']})
cpd_cancer = TabularCPD(
    variable='Cancer',
    variable_card=2,
    values=[
        [0.05, 0.02, 0.03, 0.001],
        [0.95, 0.98, 0.97, 0.999]
    ],
    evidence=['Pollution', 'Smoker'],
    evidence_card=[2, 2],
    state_names={
        'Cancer': ['True', 'False'],
        'Pollution': ['High', 'Low'],
        'Smoker': ['True', 'False']
    }
)
cpd_xray = TabularCPD(
    variable='XRay',
    variable_card=2,
    values=[
        [0.9, 0.2],
        [0.1, 0.8]
    ],
    evidence=['Cancer'],
    evidence_card=[2],
    state_names={
        'XRay': ['True', 'False'],
        'Cancer': ['True', 'False']
    }
)
cpd_dysp = TabularCPD(
    variable='Dyspnoea',
    variable_card=2,
    values=[
        [0.65, 0.3],
        [0.35, 0.7]
    ],
    evidence=['Cancer'],
    evidence_card=[2],
    state_names={
        'Dyspnoea': ['True', 'False'],
        'Cancer': ['True', 'False']
    }
)


# Associating the parameters with the model structure.
cancer_model.add_cpds(cpd_poll, cpd_smoke, cpd_cancer, cpd_xray, cpd_dysp)

# Checking if the cpds are valid for the model.
assert cancer_model.check_model()


infer = VariableElimination(cancer_model)

print(infer.query(['Cancer'], evidence={
    'XRay': 'True',
    'Dyspnoea': 'True'
}))
