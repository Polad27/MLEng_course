# task_2
ML engineering tasks

Before sharing task ensure that permission is given by Google drive owner specially for other gdrive user

Reproduce:  
```
dvc repro task_2/dvc.yaml
```

Metrics:  
```
dvc metrics show/diff
```

Plotting:  
```
dvc plots show -t .dvc/plots/scatter.json -x real -y predicted --x-label 'Real values' --y-label 'Predicted values' --title 'Predictions'
```