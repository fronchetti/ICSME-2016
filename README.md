# ICSME-ERA
This repository presents the steps needed in order to reproduce the data used in our ICSME-ERA study. Read on for the guidelines.

## Downloading Data
Here we describe how to download projects data from GitHub:

#### ISSUE AND PULL-REQUEST 
We have developed two scripts to perform this function, [issue_crawler.py](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/issue_crawler.py) and [pull_crawler.py](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/pull_crawler.py). Both are run through the terminal in a very similar way. Follow the model below and see the docstrings in each code to understand it better:

> NOTE: To run these scripts, you need to install [Scrapy](http://doc.scrapy.org/en/latest/intro/install.html) on your machine.

```bash
scrapy runspider [issue|pull]_crawler.py -a filename=rails.txt -a url=https://github.com/rails/rails -a firstpage=1 -a lastpage=10
```
At the end of the program , you must have a file like [this](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/rails.txt). If you prefer , you can use a similar alternative to download this data in Java , available at:
https://github.com/luizsusin/gitparser.

#### CONTRIBUTOR AND CONTRIBUTION
Initially , clone the repository as in the example below:

``` git clone https://github.com/ruby/ruby.git```

Then run the shellscripts [contributors.sh](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/contributors.sh), [contributions.sh](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/contributions.sh), [newcomers.sh](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/newcomers.sh) as follows:

``` ./[contributors|newcomers|contributions].sh /home/example/repository ```

## Generating charts
Before generating charts, to organize the data collected by the scripts above, we execute four scripts to organize monthly issues, pull requests, contributors and contributions dates: [issue_monthly.py](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/issue_monthly.py), [pull_monthly.py](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/pull_monthly.py),
[contribution_monthly.py](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/contribution_monthly.py) and [contributor_monthly.py](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/contributor_monthly.py).

To perform each of the codes, use:

` python [issue|pull|contribution|contributor]_monthly.py`

Finally , you can run these scripts to generate the charts: [contributor_contribution_chart.py](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/contributor_contribution_chart.py), [issue_chart.py](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/issue_chart.py) and
[pull_chart.py](https://github.com/fronchetti/ICSME-ERA-Dataset/blob/master/pull_chart.py).

` python [contributor_contribution|issue|pull]_chart.py`



