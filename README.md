# dados.br

Python Wrapper para a API [dados.gov.br](http://dados.gov.br/).

## Exemplos de Uso

```python
from dadosbr import DadosBR

api = DadosBR()
```

### Listar datasets

```python
for dataset_id in api.datasets:
    print(dataset_id)
```

### Obter dataset

```python
dataset_id = 'transferencias-totais-da-uniao-para-estados'
dataset = api.get_dataset(dataset_id)

# imprime formatos disponíveis para cada recurso
for resource in dataset.resources:
    print(resource.format_list)
    
# carrega arquivo de valores em JSON
data = dataset.resources[0].load('json')
print(data)
```

### Listar tags

```python
for tag_name in api.tags:
    print(tag_name)
```

### Obter tag

```python
tag = api.get_tag('executivo')

# imprime datasets que possuem a tag
for dataset in tag.datasets:
    print(dataset.name)
```
