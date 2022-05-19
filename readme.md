<h1 align="center">Pri reader</h1>
<h3 align="center">Algoritmo de leitura para arquivos pri/stanford</h2>
<p>Alterações do algoritmo devem ser realizadas em branchs diferentes. A branch main contem o algoritmo de execucao estavel</p>

<h2>Getting Started</h2>
<p>Antes de rodar, certifique-se que as bibliotecas necessárias foram instaladas</p>

```
pip install -r requirements.txt
```

<font color="red">ATENÇÃO</font>
<p>A biblioteca cx_freeze apresenta um error para win 32 bits. Portanto, é necessário utilizar a biblioteca mantida por terceiros</p>

```
pip uninstall cx_freeze
```

<a href="https://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_freeze"><h3>BAIXAR BIBLIOTECA cx_freeze CORRETA</h3></a>

<h2>Build</h2>
<p>Com a biblioteca instalada, utilize o a seguir para iniciar o build</p>

```
python setup.py build
```
<p>Por fim, o programa gerado estara localizado na pasta build</p>
