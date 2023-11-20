# Now defining the parameters.
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


Allergy_model = BayesianNetwork([
    ('Pollen', 'Allergy'),
    ('AteAllergicFood', 'Allergy'),
    ('Allergy', 'Sneeze'),
    ('Allergy', 'Rash')
])
cpd_poll = TabularCPD(variable='Pollen', variable_card=2, values=[
                      [0.7], [0.3]], state_names={'Pollen': ['High', 'Low']})
cpd_allfood = TabularCPD(variable='AteAllergicFood', variable_card=2, values=[
    [0.9], [0.1]], state_names={'AteAllergicFood': ['True', 'False']})
cpd_Allergy = TabularCPD(
    variable='Allergy',
    variable_card=2,
    values=[
        [0.9, 0.9, 0.9, 0.5],
        [0.1, 0.1, 0.1, 0.5]
    ],
    evidence=['Pollen', 'AteAllergicFood'],
    evidence_card=[2, 2],
    state_names={
        'Allergy': ['True', 'False'],
        'Pollen': ['High', 'Low'],
        'AteAllergicFood': ['True', 'False']
    }
)
cpd_Sneeze = TabularCPD(
    variable='Sneeze',
    variable_card=2,
    values=[
        [0.7, 0.3],
        [0.3, 0.7]
    ],
    evidence=['Allergy'],
    evidence_card=[2],
    state_names={
        'Sneeze': ['True', 'False'],
        'Allergy': ['True', 'False']
    }
)
cpd_rash = TabularCPD(
    variable='Rash',
    variable_card=2,
    values=[
        [0.9, 0.1],
        [0.1, 0.9]
    ],
    evidence=['Allergy'],
    evidence_card=[2],
    state_names={
        'Rash': ['True', 'False'],
        'Allergy': ['True', 'False']
    }
)


# Associating the parameters with the model structure.
Allergy_model.add_cpds(cpd_poll, cpd_allfood,
                       cpd_Allergy, cpd_Sneeze, cpd_rash)

# Checking if the cpds are valid for the model.
assert Allergy_model.check_model()


infer = VariableElimination(Allergy_model)

print(infer.query(['Allergy'], evidence={
    'Sneeze': 'True',
    'Rash': 'True'
}))
