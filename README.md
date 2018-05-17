# Dropbox Fetcher

## Getting Started

### Prerequisites

+ [python3](https://www.python.org/download/releases/3.0/)
+ [virtualenv](https://virtualenv.pypa.io/en/stable/)
+ [fabric](http://www.fabfile.org/) -- Note: fabric is a build tool. 

### Configure

```bash
cp config.yml{.template}
# edit config.yml 
```

### Start

Install dependencies. It requires fabric and virtualenv in py3.


```bash
fab setup
```

```bash
fab fetch
```

If you have already installed [make](https://www.gnu.org/software/make/), you can also simply type `make`, which will automatically update deps and start it 

