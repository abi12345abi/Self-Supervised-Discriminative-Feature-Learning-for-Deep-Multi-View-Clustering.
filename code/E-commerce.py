{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "collapsed_sections": [
        "7dzfbm7tw1YJ"
      ],
      "gpuType": "T4",
      "mount_file_id": "1Zin3TuHLmuOAkQ5OkcqRmRT8xRfoE2a4",
      "authorship_tag": "ABX9TyPWweR6uCxAYlfPJDi1hVG9",
      "include_colab_link":
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    },
    "accelerator": "GPU",
    "gpuClass": "standard"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Vaibhav67979/Ecommerce-product-recommendation-system/blob/main/ECommerce_Product_Recommendation_System.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#E-commerce Product recommendation System"
      ],
      "metadata": {
        "id": "EdILuyLgml_R"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "##Importing libraries"
      ],
      "metadata": {
        "id": "m-26iTTympFi"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import warnings\n",
        "warnings.filterwarnings('ignore')\n",
        "\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "from sklearn.metrics.pairwise import cosine_similarity\n",
        "\n",
        "from sklearn.metrics import mean_squared_error\n",
        "\n",
        "from scipy.sparse.linalg import svds # for sparse matrices"
      ],
      "metadata": {
        "id": "2tSOMad1mlsK"
      },
      "execution_count": 56,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Importing Dataset"
      ],
      "metadata": {
        "id": "_eRqhkyAmvFJ"
      }
    },
    {
      "cell_type": "code",
      "execution_count": 57,
      "metadata": {
        "id": "mnM0NIFemhh0"
      },
      "outputs": [],
      "source": [
        "#Import the data set\n",
        "df = pd.read_csv('/content/drive/MyDrive/ratings_Electronics.csv', header=None) #There are no headers in the data file\n",
        "\n",
        "df.columns = ['user_id', 'prod_id', 'rating', 'timestamp'] #Adding column names\n",
        "\n",
        "df = df.drop('timestamp', axis=1) #Dropping timestamp\n",
        "\n",
        "df_copy = df.copy(deep=True) #Copying the data to another dataframe"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## EDA - Exploratory Data Analysis\n",
        "\n",
        "check for -\n",
        "- shape \n",
        "- datatype\n",
        "- missing values\n",
        "\n",
        "\n",
        "finally get the summary and check\n",
        "- rating distribution.\n",
        "- number of users and products.\n",
        "- Users with highest no of ratings."
      ],
      "metadata": {
        "id": "tbUt2ZCcm2PZ"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Shape"
      ],
      "metadata": {
        "id": "P31sJRBKm7Ox"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "rows, columns = df.shape\n",
        "print(\"No of rows = \", rows)\n",
        "print(\"No of columns = \", columns)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BR0rkn1hm5Ii",
        "outputId": "b725b51e-a8d4-4786-c853-aaeb70a2da9b"
      },
      "execution_count": 58,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "No of rows =  7824482\n",
            "No of columns =  3\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Datatypes"
      ],
      "metadata": {
        "id": "BR_AWE5dm-Aw"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "df.info()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "VSZphiYsnB7h",
        "outputId": "32ed764d-62be-4b8b-b83a-942128032636"
      },
      "execution_count": 59,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "<class 'pandas.core.frame.DataFrame'>\n",
            "RangeIndex: 7824482 entries, 0 to 7824481\n",
            "Data columns (total 3 columns):\n",
            " #   Column   Dtype  \n",
            "---  ------   -----  \n",
            " 0   user_id  object \n",
            " 1   prod_id  object \n",
            " 2   rating   float64\n",
            "dtypes: float64(1), object(2)\n",
            "memory usage: 179.1+ MB\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Missing value analysis"
      ],
      "metadata": {
        "id": "nMpYlCbKm__h"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Find number of missing values in each column\n",
        "df.isna().sum()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "TmDkgSH-nG-w",
        "outputId": "b86286cf-692f-4487-a8eb-3ab912d36fea"
      },
      "execution_count": 60,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "user_id    0\n",
              "prod_id    0\n",
              "rating     0\n",
              "dtype: int64"
            ]
          },
          "metadata": {},
          "execution_count": 60
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Summary"
      ],
      "metadata": {
        "id": "NuapKpPOnIxg"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Summary statistics of 'rating' variable\n",
        "df['rating'].describe()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GykhgQNpnLB4",
        "outputId": "aee57776-f225-40d5-a337-f4ccf182a966"
      },
      "execution_count": 61,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "count    7.824482e+06\n",
              "mean     4.012337e+00\n",
              "std      1.380910e+00\n",
              "min      1.000000e+00\n",
              "25%      3.000000e+00\n",
              "50%      5.000000e+00\n",
              "75%      5.000000e+00\n",
              "max      5.000000e+00\n",
              "Name: rating, dtype: float64"
            ]
          },
          "metadata": {},
          "execution_count": 61
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Rating distribution"
      ],
      "metadata": {
        "id": "qITdLlQenOL5"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "#Create the plot and provide observations\n",
        "\n",
        "plt.figure(figsize = (12,6))\n",
        "df['rating'].value_counts(1).plot(kind='bar')\n",
        "plt.show()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 530
        },
        "id": "UGyEWlm9nN0Y",
        "outputId": "ac6635fd-e22a-4132-f6bd-9ad76a3cca48"
      },
      "execution_count": 62,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 1200x600 with 1 Axes>"
            ],
            "image/png": "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K+hK9axZs2Lp0qXR3t4+um54eDja29ujoaHhtA8HAAAAk1lBV6ojIlpaWmL16tVRX18fy5Yti82bN8fAwEA0NzdHRERTU1PMnz8/2traIuKNm5s999xzo//98ssvx/79+2P27NmxYMGC0/itAAAAwMQqOKpXrVoVhw4dig0bNkRPT08sXrw4du/ePXrzsq6urigtPXoB/JVXXoklS5aMfn333XfH3XffHVdffXXs2bPn1L8DAAAAKJKCozoi4tZbb41bb731uI/9eijX1tbGyMhI5mUAAABgUpuUd/8GAACAqUBUAwAAQJKoBgAAgCRRDQAAAEmiGgAAAJJENQAAACSJagAAAEgS1QAAAJA0s9gDAAAwOdSu21XsEaadAxtXFnsE4BS5Ug0AAABJohoAAACSRDUAAAAkiWoAAABIEtUAAACQJKoBAAAgSVQDAABAkqgGAACAJFENAAAASaIaAAAAkkQ1AAAAJIlqAAAASBLVAAAAkCSqAQAAIElUAwAAQJKoBgAAgCRRDQAAAEkziz0AAADARKldt6vYI0w7BzauLPYIZ5Qr1QAAAJAkqgEAACBJVAMAAECSqAYAAIAkUQ0AAABJohoAAACSRDUAAAAkiWoAAABIEtUAAACQJKoBAAAgSVQDAABAkqgGAACAJFENAAAASaIaAAAAkkQ1AAAAJIlqAAAASBLVAAAAkCSqAQAAIElUAwAAQJKoBgAAgCRRDQAAAEmiGgAAAJJENQAAACSJagAAAEgS1QAAAJAkqgEAACBJVAMAAECSqAYAAIAkUQ0AAABJohoAAACSRDUAAAAkiWoAAABIEtUAAACQJKoBAAAgSVQDAABAkqgGAACAJFENAAAASaIaAAAAkkQ1AAAAJIlqAAAASBLVAAAAkCSqAQAAICkV1Vu3bo3a2tooLy+P5cuXx969e0+4/cMPPxwLFy6M8vLyeM973hOPPfZYalgAAACYTAqO6p07d0ZLS0u0trbGvn37oq6uLlasWBEHDx487vZPPfVU3HTTTfGJT3wi/uu//iuuv/76uP766+PZZ5895eEBAACgmGYWusOmTZtizZo10dzcHBER27Zti127dsX27dtj3bp1x2z/hS98IX7/938/PvOZz0RExB133BFPPPFEbNmyJbZt23bc1xgcHIzBwcHRr/v6+iIior+/v9Bxi2548LVijzDtTMXjZKpznE88x/nEc5xPPMf5xHOcTzzH+cRznE+8qXqc/2rukZGRE284UoDBwcGRGTNmjDz66KNj1jc1NY1ce+21x92npqZm5J577hmzbsOGDSPvfe97x32d1tbWkYiwWCwWi8VisVgsFoulqEt3d/cJO7mgK9WHDx+OoaGhqKqqGrO+qqoqfvjDHx53n56enuNu39PTM+7rrF+/PlpaWka/Hh4ejv/93/+Nt771rVFSUlLIyCT19/dHTU1NdHd3R0VFRbHHgTPCcc504DhnOnCcMx04zifeyMhIvPrqqzFv3rwTblfw278nQllZWZSVlY1Zd8EFFxRnmGmuoqLCDy1nPcc504HjnOnAcc504DifWJWVlW+6TUE3KpszZ07MmDEjent7x6zv7e2N6urq4+5TXV1d0PYAAAAwVRQU1bNmzYqlS5dGe3v76Lrh4eFob2+PhoaG4+7T0NAwZvuIiCeeeGLc7QEAAGCqKPjt3y0tLbF69eqor6+PZcuWxebNm2NgYGD0buBNTU0xf/78aGtri4iI2267La6++ur4/Oc/HytXrowdO3bEd77znfjSl750er8TTquysrJobW095m34cDZxnDMdOM6ZDhznTAeO88mrZGTkze4PfqwtW7bEXXfdFT09PbF48eL44he/GMuXL4+IiPe///1RW1sbDzzwwOj2Dz/8cPzN3/xNHDhwIH77t3877rzzzvjDP/zD0/ZNAAAAQDGkohoAAAAo8DPVAAAAwFGiGgAAAJJENQAAACSJagAAAEgS1QAAAJAkqgEAACBJVAPTwnPPPRdr166NJUuWxNy5c2Pu3LmxZMmSWLt2bTz33HPFHg/OiMHBwRgcHCz2GAAkOHeZOvydaiLijR/aLVu2REdHR/T09ERERHV1dTQ0NMStt94aixYtKvKEkPf1r389rr/++rjssstixYoVUVVVFRERvb298cQTT0RnZ2d87WtfixUrVhR5Ujh1TzzxRNxzzz3R0dER/f39ERFRUVERDQ0N0dLSEo2NjUWeEE6d8xbOds5dphZRjR9aznp1dXVx3XXXxe23337cxz/72c/GI488Et/97ncneDI4vR588MH45Cc/GR/96EeP+ff88ccfj3/913+N+++/P2655ZYiTwp5zluYDpy7TC2iGj+0nPXe8pa3xP79++Od73zncR9//vnnY/HixfH6669P8GRwer3jHe+I2267Lf70T//0uI//4z/+Y9xzzz3xox/9aIIng9PHeQvTgXOXqcVnqokXXnghPv7xj4/7+E033eQEjCmttrY2du3aNe7ju3btiosvvngCJ4Izo6ur64Rv7/7gBz8YL7300gROBKef8xamA+cuU8vMYg9A8f3qh3a834T5oWWqu/322+NjH/tY7NmzJxobG8e8VbC9vT12794dDz30UJGnhFP3O7/zO3H//ffHnXfeedzHt2/f7rOmTHnOW5gOnLtMLd7+TTz88MPxsY99LP7gD/7ghD+0H/nIR4o8KeQ99dRT8cUvfvG4N7W57bbboqGhocgTwqnbs2dP/NEf/VFccsklx/33/Kc//Wns2rUrrrrqqiJPCnnOW5gunLtMHaKaiPBDC3C2OHDgQNx7773x9NNPH/Pv+Z/8yZ9EbW1tcQeE08B5CzCZiGoAAABIcqMyYNr7q7/6q/jjP/7jYo8BAHBSnLtMLqKaN+WHlrPdyy+/HAcOHCj2GHDGrV69Oj7wgQ8Ueww4o5y3MB04d5lc3P2bN/XSSy/5EyyclUZGRqKkpCQefPDBYo8CE2LevHlRWur36ZzdnLcwHTh3mVx8phqYtmbNmhXPPPNMvOtd7yr2KAAATFGuVHOMgYGB+OpXvxo//vGPY+7cuXHTTTfFW9/61mKPBWktLS3HXT80NBQbN24cPb43bdo0kWPBhOvu7o7W1tbYvn17sUeBU/KDH/wgnn766WhoaIiFCxfGD3/4w/jCF74Qg4ODcfPNN/uYA2eF119/PTo7O+Oiiy6KRYsWjXns//7v/+KrX/1qNDU1FWk6/n+uVBOLFi2Kb33rW3HRRRdFd3d3XHXVVfGzn/0s3vGOd8RPfvKTmDlzZjz99NPxW7/1W8UeFVJKS0ujrq4uLrjggjHrv/nNb0Z9fX2cd955UVJSEv/5n/9ZnAFhgjzzzDNx2WWXxdDQULFHgbTdu3fHddddF7Nnz47XXnstHn300Whqaoq6uroYHh6Ob37zm/H4448La6a0F154IT784Q9HV1dXlJSUxPve977YsWNHzJ07NyLe+Lvs8+bN8+/5JCGqidLS0ujp6Ym3ve1tcfPNN8d///d/x2OPPRaVlZXxi1/8Im644Yb4jd/4jXjooYeKPSqkbNy4Mb70pS/FP//zP485yTrnnHPimWeeOea3vzBV/du//dsJH//pT38af/7nf+4kjCntiiuuiA984APxd3/3d7Fjx45Yu3ZtfOpTn4rPfe5zERGxfv366OzsjMcff7zIk0LeDTfcEL/85S/jgQceiJ///OfxZ3/2Z/Hcc8/Fnj174u1vf7uonmRENWOi+tJLL41t27bFhz70odHHn3rqqbjxxhujq6uriFPCqfn2t78dN998c1xzzTXR1tYW55xzjqjmrFNaWholJSVxov+1l5SUOAljSqusrIzOzs5YsGBBDA8PR1lZWezduzeWLFkSERHPPvtsNDY2Rk9PT5Enhbyqqqr4xje+Ee95z3si4o2bq65duzYee+yxePLJJ+O8884T1ZOIW4ASEW+cZEW88fmMX72t5Ffmz58fhw4dKsZYcNpcfvnl0dnZGYcOHYr6+vp49tlnR497OFvMnTs3HnnkkRgeHj7usm/fvmKPCKfFr/79Li0tjfLy8qisrBx97Pzzz4++vr5ijQanxeuvvx4zZx69/VVJSUnce++9cc0118TVV18dL7zwQhGn49eJaiIi4oMf/GBcdtll0d/fH88///yYx1588UU3KuOsMHv27HjwwQdj/fr10djY6Le7nHWWLl0anZ2d4z7+ZlexYSqora2NH/3oR6Nfd3R0xNvf/vbRr7u6uo65QABTzcKFC+M73/nOMeu3bNkS1113XVx77bVFmIrxuPs30draOubr2bNnj/n63//93+PKK6+cyJHgjLrxxhvjfe97X3R2dsbFF19c7HHgtPnMZz4TAwMD4z6+YMGCePLJJydwIjj9PvWpT435pei73/3uMY9//etfd5Myprwbbrgh/uVf/iVuueWWYx7bsmVLDA8Px7Zt24owGcfjM9UAAACQ5O3fAAAAkCSqAQAAIElUAwAAQJKoBgAAgCRRDQAAAEmiGgAAAJJENQAAACT9PxyylOH+bvB2AAAAAElFTkSuQmCC\n"
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "The distribution is skewed to the right. Over 50% of the ratings are 5, followed by a little below 20% with 4 star ratings. And the percentages of ratings keep going down until below 10% of the ratings are 2 stars."
      ],
      "metadata": {
        "id": "EyqB_PZOnbNq"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "### No of unique users and items"
      ],
      "metadata": {
        "id": "_hoBfcSmncDJ"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Number of unique user id and product id in the data\n",
        "print('Number of unique USERS in Raw data = ', df['user_id'].nunique())\n",
        "print('Number of unique ITEMS in Raw data = ', df['prod_id'].nunique())"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "bTzXXqwrnZKh",
        "outputId": "f6dac2c0-588d-49d8-c760-258a049341aa"
      },
      "execution_count": 63,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Number of unique USERS in Raw data =  4201696\n",
            "Number of unique ITEMS in Raw data =  476002\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Users with most no of rating"
      ],
      "metadata": {
        "id": "PhOahvbHnkZJ"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Top 10 users based on rating\n",
        "most_rated = df.groupby('user_id').size().sort_values(ascending=False)[:10]\n",
        "most_rated"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "DZ80koFAngO4",
        "outputId": "45ec9525-fff5-4dbc-8319-43cbbc5df884"
      },
      "execution_count": 64,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "user_id\n",
              "A5JLAU2ARJ0BO     520\n",
              "ADLVFFE4VBT8      501\n",
              "A3OXHLG6DIBRW8    498\n",
              "A6FIAB28IS79      431\n",
              "A680RUE1FDO8B     406\n",
              "A1ODOGXEYECQQ8    380\n",
              "A36K2N527TXXJN    314\n",
              "A2AY4YUOX2N1BQ    311\n",
              "AWPODHOB4GFWL     308\n",
              "A25C2M3QF9G7OQ    296\n",
              "dtype: int64"
            ]
          },
          "metadata": {},
          "execution_count": 64
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Pre-Processing\n",
        "\n",
        "Let's take a subset of the dataset (by only keeping the users who have given 50 or more ratings) to make the dataset less sparse and easy to work with."
      ],
      "metadata": {
        "id": "ekGg2mL5oaNA"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "counts = df['user_id'].value_counts()\n",
        "df_final = df[df['user_id'].isin(counts[counts >= 50].index)]"
      ],
      "metadata": {
        "id": "k3T1weHIodDw"
      },
      "execution_count": 65,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "print('The number of observations in the final data =', len(df_final))\n",
        "print('Number of unique USERS in the final data = ', df_final['user_id'].nunique())\n",
        "print('Number of unique PRODUCTS in the final data = ', df_final['prod_id'].nunique())"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KDnxTiwUordB",
        "outputId": "24eb9a76-ec91-46e9-92b7-397d4adaa25f"
      },
      "execution_count": 66,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "The number of observations in the final data = 125871\n",
            "Number of unique USERS in the final data =  1540\n",
            "Number of unique PRODUCTS in the final data =  48190\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "- The dataframe **df_final has users who have rated 50 or more items**\n",
        "- **We will use df_final to build recommendation systems**"
      ],
      "metadata": {
        "id": "tsmGpFwqocrg"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Checking the density of the rating matrix"
      ],
      "metadata": {
        "id": "k6t4Ee-Oo0vD"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "#Creating the interaction matrix of products and users based on ratings and replacing NaN value with 0\n",
        "final_ratings_matrix = df_final.pivot(index = 'user_id', columns ='prod_id', values = 'rating').fillna(0)\n",
        "print('Shape of final_ratings_matrix: ', final_ratings_matrix.shape)\n",
        "\n",
        "#Finding the number of non-zero entries in the interaction matrix \n",
        "given_num_of_ratings = np.count_nonzero(final_ratings_matrix)\n",
        "print('given_num_of_ratings = ', given_num_of_ratings)\n",
        "\n",
        "#Finding the possible number of ratings as per the number of users and products\n",
        "possible_num_of_ratings = final_ratings_matrix.shape[0] * final_ratings_matrix.shape[1]\n",
        "print('possible_num_of_ratings = ', possible_num_of_ratings)\n",
        "\n",
        "#Density of ratings\n",
        "density = (given_num_of_ratings/possible_num_of_ratings)\n",
        "density *= 100\n",
        "print ('density: {:4.2f}%'.format(density))\n",
        "\n",
        "final_ratings_matrix.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 400
        },
        "id": "Q3kGwNuyoxiR",
        "outputId": "d67b95ea-2336-4268-b89b-044fc329ef85"
      },
      "execution_count": 67,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Shape of final_ratings_matrix:  (1540, 48190)\n",
            "given_num_of_ratings =  125871\n",
            "possible_num_of_ratings =  74212600\n",
            "density: 0.17%\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "prod_id         0594451647  0594481813  0970407998  0972683275  1400501466  \\\n",
              "user_id                                                                      \n",
              "A100UD67AHFODS         0.0         0.0         0.0         0.0         0.0   \n",
              "A100WO06OQR8BQ         0.0         0.0         0.0         0.0         0.0   \n",
              "A105S56ODHGJEK         0.0         0.0         0.0         0.0         0.0   \n",
              "A105TOJ6LTVMBG         0.0         0.0         0.0         0.0         0.0   \n",
              "A10AFVU66A79Y1         0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id         1400501520  1400501776  1400532620  1400532655  140053271X  \\\n",
              "user_id                                                                      \n",
              "A100UD67AHFODS         0.0         0.0         0.0         0.0         0.0   \n",
              "A100WO06OQR8BQ         0.0         0.0         0.0         0.0         0.0   \n",
              "A105S56ODHGJEK         0.0         0.0         0.0         0.0         0.0   \n",
              "A105TOJ6LTVMBG         0.0         0.0         0.0         0.0         0.0   \n",
              "A10AFVU66A79Y1         0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id         ...  B00L5YZCCG  B00L8I6SFY  B00L8QCVL6  B00LA6T0LS  \\\n",
              "user_id         ...                                                   \n",
              "A100UD67AHFODS  ...         0.0         0.0         0.0         0.0   \n",
              "A100WO06OQR8BQ  ...         0.0         0.0         0.0         0.0   \n",
              "A105S56ODHGJEK  ...         0.0         0.0         0.0         0.0   \n",
              "A105TOJ6LTVMBG  ...         0.0         0.0         0.0         0.0   \n",
              "A10AFVU66A79Y1  ...         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id         B00LBZ1Z7K  B00LED02VY  B00LGN7Y3G  B00LGQ6HL8  B00LI4ZZO8  \\\n",
              "user_id                                                                      \n",
              "A100UD67AHFODS         0.0         0.0         0.0         0.0         0.0   \n",
              "A100WO06OQR8BQ         0.0         0.0         0.0         0.0         0.0   \n",
              "A105S56ODHGJEK         0.0         0.0         0.0         0.0         0.0   \n",
              "A105TOJ6LTVMBG         0.0         0.0         0.0         0.0         0.0   \n",
              "A10AFVU66A79Y1         0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id         B00LKG1MC8  \n",
              "user_id                     \n",
              "A100UD67AHFODS         0.0  \n",
              "A100WO06OQR8BQ         0.0  \n",
              "A105S56ODHGJEK         0.0  \n",
              "A105TOJ6LTVMBG         0.0  \n",
              "A10AFVU66A79Y1         0.0  \n",
              "\n",
              "[5 rows x 48190 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-c67712a7-be22-4715-b4d6-76c5f2d15918\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th>prod_id</th>\n",
              "      <th>0594451647</th>\n",
              "      <th>0594481813</th>\n",
              "      <th>0970407998</th>\n",
              "      <th>0972683275</th>\n",
              "      <th>1400501466</th>\n",
              "      <th>1400501520</th>\n",
              "      <th>1400501776</th>\n",
              "      <th>1400532620</th>\n",
              "      <th>1400532655</th>\n",
              "      <th>140053271X</th>\n",
              "      <th>...</th>\n",
              "      <th>B00L5YZCCG</th>\n",
              "      <th>B00L8I6SFY</th>\n",
              "      <th>B00L8QCVL6</th>\n",
              "      <th>B00LA6T0LS</th>\n",
              "      <th>B00LBZ1Z7K</th>\n",
              "      <th>B00LED02VY</th>\n",
              "      <th>B00LGN7Y3G</th>\n",
              "      <th>B00LGQ6HL8</th>\n",
              "      <th>B00LI4ZZO8</th>\n",
              "      <th>B00LKG1MC8</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>user_id</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>A100UD67AHFODS</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>A100WO06OQR8BQ</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>A105S56ODHGJEK</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>A105TOJ6LTVMBG</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>A10AFVU66A79Y1</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 48190 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-c67712a7-be22-4715-b4d6-76c5f2d15918')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-c67712a7-be22-4715-b4d6-76c5f2d15918 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-c67712a7-be22-4715-b4d6-76c5f2d15918');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 67
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Rank Based Recommendation System "
      ],
      "metadata": {
        "id": "7dzfbm7tw1YJ"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "#Calculate the average rating for each product \n",
        "average_rating = df_final.groupby('prod_id').mean()['rating']\n",
        "\n",
        "#Calculate the count of ratings for each product\n",
        "count_rating = df_final.groupby('prod_id').count()['rating']\n",
        "\n",
        "#Create a dataframe with calculated average and count of ratings\n",
        "final_rating = pd.DataFrame({'avg_rating':average_rating, 'rating_count':count_rating})\n",
        "\n",
        "#Sort the dataframe by average of ratings\n",
        "final_rating = final_rating.sort_values(by='avg_rating',ascending=False)\n",
        "\n",
        "final_rating.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 237
        },
        "id": "me4iOm2ow9Yx",
        "outputId": "8c2ba921-f35a-4e1a-8bf1-fb7e3cbdefeb"
      },
      "execution_count": 36,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "            avg_rating  rating_count\n",
              "prod_id                             \n",
              "0594451647         5.0             1\n",
              "B003RRY9RS         5.0             1\n",
              "B003RR95Q8         5.0             1\n",
              "B003RIPMZU         5.0             1\n",
              "B003RFRNYQ         5.0             2"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-f88e885f-a197-4f40-927d-3fc5c185cf74\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>avg_rating</th>\n",
              "      <th>rating_count</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>prod_id</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0594451647</th>\n",
              "      <td>5.0</td>\n",
              "      <td>1</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>B003RRY9RS</th>\n",
              "      <td>5.0</td>\n",
              "      <td>1</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>B003RR95Q8</th>\n",
              "      <td>5.0</td>\n",
              "      <td>1</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>B003RIPMZU</th>\n",
              "      <td>5.0</td>\n",
              "      <td>1</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>B003RFRNYQ</th>\n",
              "      <td>5.0</td>\n",
              "      <td>2</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-f88e885f-a197-4f40-927d-3fc5c185cf74')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-f88e885f-a197-4f40-927d-3fc5c185cf74 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-f88e885f-a197-4f40-927d-3fc5c185cf74');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 36
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#defining a function to get the top n products based on highest average rating and minimum interactions\n",
        "def top_n_products(final_rating, n, min_interaction):\n",
        "    \n",
        "    #Finding products with minimum number of interactions\n",
        "    recommendations = final_rating[final_rating['rating_count']>min_interaction]\n",
        "    \n",
        "    #Sorting values w.r.t average rating \n",
        "    recommendations = recommendations.sort_values('avg_rating',ascending=False)\n",
        "    \n",
        "    return recommendations.index[:n]"
      ],
      "metadata": {
        "id": "OhUAXTtgw-8Q"
      },
      "execution_count": 37,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Recommending top 5 products with 50 minimum interactions based on popularity"
      ],
      "metadata": {
        "id": "wem_XKyUxGEw"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "list(top_n_products(final_rating, 5, 50))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "5Tp7b5ByxCl4",
        "outputId": "030923b7-3903-45e1-dbb8-49c91dbeb65a"
      },
      "execution_count": 38,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "['B001TH7GUU', 'B003ES5ZUU', 'B0019EHU8G', 'B006W8U2MU', 'B000QUUFRW']"
            ]
          },
          "metadata": {},
          "execution_count": 38
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Recommending top 5 products with 100 minimum interactions based on popularity"
      ],
      "metadata": {
        "id": "1dMFKudcxJW5"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "list(top_n_products(final_rating, 5, 100))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "-3lUEc76xL_Y",
        "outputId": "a4e4ec84-a9b0-4900-a105-26c073637433"
      },
      "execution_count": 39,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "['B003ES5ZUU', 'B000N99BBC', 'B007WTAJTO', 'B002V88HFE', 'B004CLYEDC']"
            ]
          },
          "metadata": {},
          "execution_count": 39
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Collaborative Filtering based Recommendation System "
      ],
      "metadata": {
        "id": "2ykt7MfyXw1d"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "## User based collaborative filtering"
      ],
      "metadata": {
        "id": "hXdPQ-0PcUVE"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "final_ratings_matrix.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 331
        },
        "id": "jVP_TvuqX17T",
        "outputId": "974075eb-a07a-480a-fa2d-169b15c4bc1f"
      },
      "execution_count": 114,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "prod_id         0594451647  0594481813  0970407998  0972683275  1400501466  \\\n",
              "user_id                                                                      \n",
              "A100UD67AHFODS         0.0         0.0         0.0         0.0         0.0   \n",
              "A100WO06OQR8BQ         0.0         0.0         0.0         0.0         0.0   \n",
              "A105S56ODHGJEK         0.0         0.0         0.0         0.0         0.0   \n",
              "A105TOJ6LTVMBG         0.0         0.0         0.0         0.0         0.0   \n",
              "A10AFVU66A79Y1         0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id         1400501520  1400501776  1400532620  1400532655  140053271X  \\\n",
              "user_id                                                                      \n",
              "A100UD67AHFODS         0.0         0.0         0.0         0.0         0.0   \n",
              "A100WO06OQR8BQ         0.0         0.0         0.0         0.0         0.0   \n",
              "A105S56ODHGJEK         0.0         0.0         0.0         0.0         0.0   \n",
              "A105TOJ6LTVMBG         0.0         0.0         0.0         0.0         0.0   \n",
              "A10AFVU66A79Y1         0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id         ...  B00L5YZCCG  B00L8I6SFY  B00L8QCVL6  B00LA6T0LS  \\\n",
              "user_id         ...                                                   \n",
              "A100UD67AHFODS  ...         0.0         0.0         0.0         0.0   \n",
              "A100WO06OQR8BQ  ...         0.0         0.0         0.0         0.0   \n",
              "A105S56ODHGJEK  ...         0.0         0.0         0.0         0.0   \n",
              "A105TOJ6LTVMBG  ...         0.0         0.0         0.0         0.0   \n",
              "A10AFVU66A79Y1  ...         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id         B00LBZ1Z7K  B00LED02VY  B00LGN7Y3G  B00LGQ6HL8  B00LI4ZZO8  \\\n",
              "user_id                                                                      \n",
              "A100UD67AHFODS         0.0         0.0         0.0         0.0         0.0   \n",
              "A100WO06OQR8BQ         0.0         0.0         0.0         0.0         0.0   \n",
              "A105S56ODHGJEK         0.0         0.0         0.0         0.0         0.0   \n",
              "A105TOJ6LTVMBG         0.0         0.0         0.0         0.0         0.0   \n",
              "A10AFVU66A79Y1         0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id         B00LKG1MC8  \n",
              "user_id                     \n",
              "A100UD67AHFODS         0.0  \n",
              "A100WO06OQR8BQ         0.0  \n",
              "A105S56ODHGJEK         0.0  \n",
              "A105TOJ6LTVMBG         0.0  \n",
              "A10AFVU66A79Y1         0.0  \n",
              "\n",
              "[5 rows x 48190 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-0066f289-93ee-45a9-9ef4-d972d51f5f9b\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th>prod_id</th>\n",
              "      <th>0594451647</th>\n",
              "      <th>0594481813</th>\n",
              "      <th>0970407998</th>\n",
              "      <th>0972683275</th>\n",
              "      <th>1400501466</th>\n",
              "      <th>1400501520</th>\n",
              "      <th>1400501776</th>\n",
              "      <th>1400532620</th>\n",
              "      <th>1400532655</th>\n",
              "      <th>140053271X</th>\n",
              "      <th>...</th>\n",
              "      <th>B00L5YZCCG</th>\n",
              "      <th>B00L8I6SFY</th>\n",
              "      <th>B00L8QCVL6</th>\n",
              "      <th>B00LA6T0LS</th>\n",
              "      <th>B00LBZ1Z7K</th>\n",
              "      <th>B00LED02VY</th>\n",
              "      <th>B00LGN7Y3G</th>\n",
              "      <th>B00LGQ6HL8</th>\n",
              "      <th>B00LI4ZZO8</th>\n",
              "      <th>B00LKG1MC8</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>user_id</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>A100UD67AHFODS</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>A100WO06OQR8BQ</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>A105S56ODHGJEK</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>A105TOJ6LTVMBG</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>A10AFVU66A79Y1</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 48190 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-0066f289-93ee-45a9-9ef4-d972d51f5f9b')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-0066f289-93ee-45a9-9ef4-d972d51f5f9b button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-0066f289-93ee-45a9-9ef4-d972d51f5f9b');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 114
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Here, user_id (index) is of the object data type. We will replace the user_id by numbers starting from 0 to 1539 (for all user ids) so that the index is of integer type and represents a user id in the same format"
      ],
      "metadata": {
        "id": "JVADHXQHX7_S"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "final_ratings_matrix['user_index'] = np.arange(0, final_ratings_matrix.shape[0])\n",
        "final_ratings_matrix.set_index(['user_index'], inplace=True)\n",
        "\n",
        "# Actual ratings given by users\n",
        "final_ratings_matrix.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 331
        },
        "id": "CFAS5YaPX9aD",
        "outputId": "a5f2ae4e-478b-410d-de10-2bfacc72134e"
      },
      "execution_count": 115,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "prod_id     0594451647  0594481813  0970407998  0972683275  1400501466  \\\n",
              "user_index                                                               \n",
              "0                  0.0         0.0         0.0         0.0         0.0   \n",
              "1                  0.0         0.0         0.0         0.0         0.0   \n",
              "2                  0.0         0.0         0.0         0.0         0.0   \n",
              "3                  0.0         0.0         0.0         0.0         0.0   \n",
              "4                  0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id     1400501520  1400501776  1400532620  1400532655  140053271X  ...  \\\n",
              "user_index                                                              ...   \n",
              "0                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "1                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "2                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "3                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "4                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "\n",
              "prod_id     B00L5YZCCG  B00L8I6SFY  B00L8QCVL6  B00LA6T0LS  B00LBZ1Z7K  \\\n",
              "user_index                                                               \n",
              "0                  0.0         0.0         0.0         0.0         0.0   \n",
              "1                  0.0         0.0         0.0         0.0         0.0   \n",
              "2                  0.0         0.0         0.0         0.0         0.0   \n",
              "3                  0.0         0.0         0.0         0.0         0.0   \n",
              "4                  0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id     B00LED02VY  B00LGN7Y3G  B00LGQ6HL8  B00LI4ZZO8  B00LKG1MC8  \n",
              "user_index                                                              \n",
              "0                  0.0         0.0         0.0         0.0         0.0  \n",
              "1                  0.0         0.0         0.0         0.0         0.0  \n",
              "2                  0.0         0.0         0.0         0.0         0.0  \n",
              "3                  0.0         0.0         0.0         0.0         0.0  \n",
              "4                  0.0         0.0         0.0         0.0         0.0  \n",
              "\n",
              "[5 rows x 48190 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-f2dcd8be-876f-42ad-8f51-5507461ffe26\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th>prod_id</th>\n",
              "      <th>0594451647</th>\n",
              "      <th>0594481813</th>\n",
              "      <th>0970407998</th>\n",
              "      <th>0972683275</th>\n",
              "      <th>1400501466</th>\n",
              "      <th>1400501520</th>\n",
              "      <th>1400501776</th>\n",
              "      <th>1400532620</th>\n",
              "      <th>1400532655</th>\n",
              "      <th>140053271X</th>\n",
              "      <th>...</th>\n",
              "      <th>B00L5YZCCG</th>\n",
              "      <th>B00L8I6SFY</th>\n",
              "      <th>B00L8QCVL6</th>\n",
              "      <th>B00LA6T0LS</th>\n",
              "      <th>B00LBZ1Z7K</th>\n",
              "      <th>B00LED02VY</th>\n",
              "      <th>B00LGN7Y3G</th>\n",
              "      <th>B00LGQ6HL8</th>\n",
              "      <th>B00LI4ZZO8</th>\n",
              "      <th>B00LKG1MC8</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>user_index</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 48190 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-f2dcd8be-876f-42ad-8f51-5507461ffe26')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-f2dcd8be-876f-42ad-8f51-5507461ffe26 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-f2dcd8be-876f-42ad-8f51-5507461ffe26');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 115
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Function to find Similar users and their similarity scores"
      ],
      "metadata": {
        "id": "XF4rlGcsb8-D"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# defining a function to get similar users\n",
        "def similar_users(user_index, interactions_matrix):\n",
        "    similarity = []\n",
        "    for user in range(0, interactions_matrix.shape[0]): #  .shape[0] gives number of rows\n",
        "        \n",
        "        #finding cosine similarity between the user_id and each user\n",
        "        sim = cosine_similarity([interactions_matrix.loc[user_index]], [interactions_matrix.loc[user]])\n",
        "        \n",
        "        #Appending the user and the corresponding similarity score with user_id as a tuple\n",
        "        similarity.append((user,sim))\n",
        "        \n",
        "    similarity.sort(key=lambda x: x[1], reverse=True)\n",
        "    most_similar_users = [tup[0] for tup in similarity] #Extract the user from each tuple in the sorted list\n",
        "    similarity_score = [tup[1] for tup in similarity] ##Extracting the similarity score from each tuple in the sorted list\n",
        "   \n",
        "    #Remove the original user and its similarity score and keep only other similar users \n",
        "    most_similar_users.remove(user_index)\n",
        "    similarity_score.remove(similarity_score[0])\n",
        "       \n",
        "    return most_similar_users, similarity_score"
      ],
      "metadata": {
        "id": "OlJyXfxTX_I7"
      },
      "execution_count": 46,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#### Finding out top 10 similar users to the user index 3 and their similarity score"
      ],
      "metadata": {
        "id": "t8YQa3aSYDQc"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "similar = similar_users(3,final_ratings_matrix)[0][0:10]\n",
        "similar"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BevLPijqYFYK",
        "outputId": "1d04cdab-d446-4726-b85b-99eb2f94a316"
      },
      "execution_count": 47,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "[320, 12, 793, 261, 156, 1493, 1250, 567, 753, 1360]"
            ]
          },
          "metadata": {},
          "execution_count": 47
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Print the similarity score\n",
        "similar_users(3,final_ratings_matrix)[1][0:10]"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GbbgcMaKYJXz",
        "outputId": "e1c5e877-d8a0-4f92-fdec-af4562542c17"
      },
      "execution_count": 48,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "[array([[0.05662371]]),\n",
              " array([[0.05549645]]),\n",
              " array([[0.05098326]]),\n",
              " array([[0.05024185]]),\n",
              " array([[0.05003874]]),\n",
              " array([[0.04930111]]),\n",
              " array([[0.04889354]]),\n",
              " array([[0.04672744]]),\n",
              " array([[0.04637283]]),\n",
              " array([[0.04492668]])]"
            ]
          },
          "metadata": {},
          "execution_count": 48
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#### Finding out top 10 similar users to the user index 1521 and their similarity score"
      ],
      "metadata": {
        "id": "ozHlmOBmYHeT"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "similar = similar_users(1521, final_ratings_matrix)[0][0:10]\n",
        "similar"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "S8JFRg9XYPE8",
        "outputId": "66801699-abb6-4da2-8c2d-86a3ccf6917c"
      },
      "execution_count": 49,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "[991, 1065, 1012, 1402, 1371, 1278, 1518, 692, 785, 161]"
            ]
          },
          "metadata": {},
          "execution_count": 49
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Print the similarity score\n",
        "similar_users(1521,final_ratings_matrix)[1][0:10]"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "tsnilvK-YTST",
        "outputId": "58afdd6c-1f95-481a-94d9-1ef9269e7cc0"
      },
      "execution_count": 50,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "[array([[0.10889304]]),\n",
              " array([[0.10538068]]),\n",
              " array([[0.1026758]]),\n",
              " array([[0.09418291]]),\n",
              " array([[0.09149062]]),\n",
              " array([[0.09135361]]),\n",
              " array([[0.09028898]]),\n",
              " array([[0.08735684]]),\n",
              " array([[0.08673386]]),\n",
              " array([[0.08478815]])]"
            ]
          },
          "metadata": {},
          "execution_count": 50
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Function to recommend products"
      ],
      "metadata": {
        "id": "qXSJzV0EcFcC"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# defining the recommendations function to get recommendations by using the similar users' preferences\n",
        "def recommendations(user_index, num_of_products, interactions_matrix):\n",
        "    \n",
        "    #Saving similar users using the function similar_users defined above\n",
        "    most_similar_users = similar_users(user_index, interactions_matrix)[0]\n",
        "    \n",
        "    #Finding product IDs with which the user_id has interacted\n",
        "    prod_ids = set(list(interactions_matrix.columns[np.where(interactions_matrix.loc[user_index] > 0)]))\n",
        "    recommendations = []\n",
        "    \n",
        "    observed_interactions = prod_ids.copy()\n",
        "    for similar_user in most_similar_users:\n",
        "        if len(recommendations) < num_of_products:\n",
        "            \n",
        "            #Finding 'n' products which have been rated by similar users but not by the user_id\n",
        "            similar_user_prod_ids = set(list(interactions_matrix.columns[np.where(interactions_matrix.loc[similar_user] > 0)]))\n",
        "            recommendations.extend(list(similar_user_prod_ids.difference(observed_interactions)))\n",
        "            observed_interactions = observed_interactions.union(similar_user_prod_ids)\n",
        "        else:\n",
        "            break\n",
        "    \n",
        "    return recommendations[:num_of_products]"
      ],
      "metadata": {
        "id": "uq6Wzl1kYX3U"
      },
      "execution_count": 51,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#### Recommend 5 products to user index 3 based on similarity based collaborative filtering"
      ],
      "metadata": {
        "id": "p6IzV6fTYbhW"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "recommendations(3,5,final_ratings_matrix)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "KBF7-RKIYcVL",
        "outputId": "38957d77-0e8e-419a-e958-2e4e835d49ed"
      },
      "execution_count": 52,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "['B001TAAVP4', 'B0016E5X5Q', 'B0054U6CEE', 'B00006IW1X', 'B000HWVOFQ']"
            ]
          },
          "metadata": {},
          "execution_count": 52
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#### Recommend 5 products to user index 1521 based on similarity based collaborative filtering"
      ],
      "metadata": {
        "id": "pNxqmWlAYoiK"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "recommendations(1521,5,final_ratings_matrix)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Gs0zuFFQYpQi",
        "outputId": "319dcde7-75fd-4978-f790-3e2fc9cff683"
      },
      "execution_count": 53,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "['B007X3VEUW', 'B005TDWUII', 'B0040XQ7PK', 'B009O7XGCY', 'B00A7PPLP2']"
            ]
          },
          "metadata": {},
          "execution_count": 53
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Model based Collaborative Filtering: Singular Value Decomposition \n",
        "\n",
        "**We have seen above that the interaction matrix is highly sparse. SVD is best to apply on a large sparse matrix. Note that for sparse matrices, we can use the sparse.linalg.svds() function to perform the decomposition**\n",
        "\n",
        "Also, we will use **k=50 latent features** to predict rating of products"
      ],
      "metadata": {
        "id": "B9fOdRwUdbKa"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "## CSR matrix"
      ],
      "metadata": {
        "id": "RXgHZdNYmoKD"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "from scipy.sparse import csr_matrix\n",
        "final_ratings_sparse = csr_matrix(final_ratings_matrix.values)\n"
      ],
      "metadata": {
        "id": "6yHPX6rkfeY8"
      },
      "execution_count": 125,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## SVD"
      ],
      "metadata": {
        "id": "K2oQ3Fjlmrs7"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Singular Value Decomposition\n",
        "U, s, Vt = svds(final_ratings_sparse, k = 50) # here k is the number of latent features\n",
        "\n",
        "# Construct diagonal array in SVD\n",
        "sigma = np.diag(s)"
      ],
      "metadata": {
        "id": "D8BDZzhXdhKa"
      },
      "execution_count": 126,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "U.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "IqVjx_ebfkZD",
        "outputId": "412703cf-e6c6-4322-d1e3-5e45d2a27957"
      },
      "execution_count": 127,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(1540, 50)"
            ]
          },
          "metadata": {},
          "execution_count": 127
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "sigma.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "i0pbUMYXfnvq",
        "outputId": "af7129f1-371e-454e-80dc-66f960870ef9"
      },
      "execution_count": 128,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(50, 50)"
            ]
          },
          "metadata": {},
          "execution_count": 128
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "Vt.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "9eK_VGtwfoRJ",
        "outputId": "9d84b451-249f-4951-9f17-354e3178da9d"
      },
      "execution_count": 129,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(50, 48190)"
            ]
          },
          "metadata": {},
          "execution_count": 129
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Now, let's regenerate the original matrix using U, Sigma, and Vt matrices. The resulting matrix would be the predicted ratings for all users and products"
      ],
      "metadata": {
        "id": "FSE_KKudftuk"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Predicting ratings"
      ],
      "metadata": {
        "id": "BVnvgQkwmvfL"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) \n",
        "\n",
        "# Predicted ratings\n",
        "preds_df = pd.DataFrame(abs(all_user_predicted_ratings), columns = final_ratings_matrix.columns)\n",
        "preds_df.head()\n",
        "preds_matrix = csr_matrix(preds_df.values)"
      ],
      "metadata": {
        "id": "hURsS2H3fuby"
      },
      "execution_count": 130,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Function to recommend products"
      ],
      "metadata": {
        "id": "jRS4Fndbfx-c"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import numpy as np\n",
        "\n",
        "def recommend_items(user_index, interactions_matrix, preds_matrix, num_recommendations):\n",
        "    \n",
        "    # Get the user's ratings from the actual and predicted interaction matrices\n",
        "    user_ratings = interactions_matrix[user_index,:].toarray().reshape(-1)\n",
        "    user_predictions = preds_matrix[user_index,:].toarray().reshape(-1)\n",
        "\n",
        "    #Creating a dataframe with actual and predicted ratings columns\n",
        "    temp = pd.DataFrame({'user_ratings': user_ratings, 'user_predictions': user_predictions})\n",
        "    temp['Recommended Products'] = np.arange(len(user_ratings))\n",
        "    temp = temp.set_index('Recommended Products')\n",
        "    \n",
        "    #Filtering the dataframe where actual ratings are 0 which implies that the user has not interacted with that product\n",
        "    temp = temp.loc[temp.user_ratings == 0]   \n",
        "    \n",
        "    #Recommending products with top predicted ratings\n",
        "    temp = temp.sort_values('user_predictions',ascending=False)#Sort the dataframe by user_predictions in descending order\n",
        "    print('\\nBelow are the recommended products for user(user_id = {}):\\n'.format(user_index))\n",
        "    print(temp['user_predictions'].head(num_recommendations))\n"
      ],
      "metadata": {
        "id": "IMI2d1sXiILL"
      },
      "execution_count": 131,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Recommending top 5 products to user id 121"
      ],
      "metadata": {
        "id": "ni3knh42f5qa"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "#Enter 'user index' and 'num_recommendations' for the user\n",
        "recommend_items(121,final_ratings_sparse,preds_matrix,5)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "IxLbE4G6f80b",
        "outputId": "9db9e9ee-3999-4a06-9a73-ead583865ded"
      },
      "execution_count": 133,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Below are the recommended products for user(user_id = 121):\n",
            "\n",
            "Recommended Products\n",
            "28761    2.414390\n",
            "39003    1.521306\n",
            "41420    1.309224\n",
            "40158    1.200111\n",
            "33819    1.126866\n",
            "Name: user_predictions, dtype: float64\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### Recommending top 10 products to user id 100"
      ],
      "metadata": {
        "id": "913jkZjPm9qr"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "recommend_items(100,final_ratings_sparse,preds_matrix,10)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "QVBWustNlnXh",
        "outputId": "19185fbe-765e-4ac4-cf1c-07a805824a98"
      },
      "execution_count": 134,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Below are the recommended products for user(user_id = 100):\n",
            "\n",
            "Recommended Products\n",
            "11078    1.624746\n",
            "16159    1.132730\n",
            "10276    1.047888\n",
            "22210    0.955049\n",
            "18887    0.879705\n",
            "41618    0.854430\n",
            "45008    0.816153\n",
            "43419    0.803755\n",
            "28761    0.748799\n",
            "14791    0.748797\n",
            "Name: user_predictions, dtype: float64\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Evaluating the model"
      ],
      "metadata": {
        "id": "th5-d8wFmD9r"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "final_ratings_matrix['user_index'] = np.arange(0, final_ratings_matrix.shape[0])\n",
        "final_ratings_matrix.set_index(['user_index'], inplace=True)\n",
        "\n",
        "# Actual ratings given by users\n",
        "final_ratings_matrix.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 331
        },
        "id": "iZYhmD6hmEPz",
        "outputId": "b2c5355a-3e17-4536-ed75-ef854c48be66"
      },
      "execution_count": 135,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "prod_id     0594451647  0594481813  0970407998  0972683275  1400501466  \\\n",
              "user_index                                                               \n",
              "0                  0.0         0.0         0.0         0.0         0.0   \n",
              "1                  0.0         0.0         0.0         0.0         0.0   \n",
              "2                  0.0         0.0         0.0         0.0         0.0   \n",
              "3                  0.0         0.0         0.0         0.0         0.0   \n",
              "4                  0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id     1400501520  1400501776  1400532620  1400532655  140053271X  ...  \\\n",
              "user_index                                                              ...   \n",
              "0                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "1                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "2                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "3                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "4                  0.0         0.0         0.0         0.0         0.0  ...   \n",
              "\n",
              "prod_id     B00L5YZCCG  B00L8I6SFY  B00L8QCVL6  B00LA6T0LS  B00LBZ1Z7K  \\\n",
              "user_index                                                               \n",
              "0                  0.0         0.0         0.0         0.0         0.0   \n",
              "1                  0.0         0.0         0.0         0.0         0.0   \n",
              "2                  0.0         0.0         0.0         0.0         0.0   \n",
              "3                  0.0         0.0         0.0         0.0         0.0   \n",
              "4                  0.0         0.0         0.0         0.0         0.0   \n",
              "\n",
              "prod_id     B00LED02VY  B00LGN7Y3G  B00LGQ6HL8  B00LI4ZZO8  B00LKG1MC8  \n",
              "user_index                                                              \n",
              "0                  0.0         0.0         0.0         0.0         0.0  \n",
              "1                  0.0         0.0         0.0         0.0         0.0  \n",
              "2                  0.0         0.0         0.0         0.0         0.0  \n",
              "3                  0.0         0.0         0.0         0.0         0.0  \n",
              "4                  0.0         0.0         0.0         0.0         0.0  \n",
              "\n",
              "[5 rows x 48190 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-c532dfa7-e391-4b2b-a0f1-ee15e1212d49\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th>prod_id</th>\n",
              "      <th>0594451647</th>\n",
              "      <th>0594481813</th>\n",
              "      <th>0970407998</th>\n",
              "      <th>0972683275</th>\n",
              "      <th>1400501466</th>\n",
              "      <th>1400501520</th>\n",
              "      <th>1400501776</th>\n",
              "      <th>1400532620</th>\n",
              "      <th>1400532655</th>\n",
              "      <th>140053271X</th>\n",
              "      <th>...</th>\n",
              "      <th>B00L5YZCCG</th>\n",
              "      <th>B00L8I6SFY</th>\n",
              "      <th>B00L8QCVL6</th>\n",
              "      <th>B00LA6T0LS</th>\n",
              "      <th>B00LBZ1Z7K</th>\n",
              "      <th>B00LED02VY</th>\n",
              "      <th>B00LGN7Y3G</th>\n",
              "      <th>B00LGQ6HL8</th>\n",
              "      <th>B00LI4ZZO8</th>\n",
              "      <th>B00LKG1MC8</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>user_index</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 48190 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-c532dfa7-e391-4b2b-a0f1-ee15e1212d49')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-c532dfa7-e391-4b2b-a0f1-ee15e1212d49 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-c532dfa7-e391-4b2b-a0f1-ee15e1212d49');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 135
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "average_rating = final_ratings_matrix.mean()\n",
        "average_rating.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "3cTXMcS0mNni",
        "outputId": "c3d0c15b-e3fc-42ab-a66d-88db90de364c"
      },
      "execution_count": 136,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "prod_id\n",
              "0594451647    0.003247\n",
              "0594481813    0.001948\n",
              "0970407998    0.003247\n",
              "0972683275    0.012338\n",
              "1400501466    0.012987\n",
              "dtype: float64"
            ]
          },
          "metadata": {},
          "execution_count": 136
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "preds_df.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 299
        },
        "id": "-QoOy6c2mQIj",
        "outputId": "fa3504da-4f29-42f5-d747-79f4886b80d6"
      },
      "execution_count": 137,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "prod_id  0594451647  0594481813  0970407998  0972683275  1400501466  \\\n",
              "0          0.005086    0.002178    0.003668    0.040843    0.009640   \n",
              "1          0.002286    0.010898    0.000724    0.130259    0.007506   \n",
              "2          0.001655    0.002675    0.007355    0.007264    0.005152   \n",
              "3          0.001856    0.011019    0.005910    0.014134    0.000179   \n",
              "4          0.001115    0.002670    0.011018    0.014434    0.010319   \n",
              "\n",
              "prod_id  1400501520  1400501776  1400532620  1400532655  140053271X  ...  \\\n",
              "0          0.006808    0.020659    0.000649    0.020331    0.005633  ...   \n",
              "1          0.003350    0.063711    0.000674    0.016111    0.002433  ...   \n",
              "2          0.003986    0.003480    0.006961    0.006606    0.002719  ...   \n",
              "3          0.001877    0.005391    0.001709    0.004968    0.001402  ...   \n",
              "4          0.006002    0.017151    0.003726    0.001404    0.005645  ...   \n",
              "\n",
              "prod_id  B00L5YZCCG  B00L8I6SFY  B00L8QCVL6  B00LA6T0LS  B00LBZ1Z7K  \\\n",
              "0          0.000238    0.061477    0.001214    0.123433    0.028490   \n",
              "1          0.000038    0.013766    0.001473    0.025588    0.042103   \n",
              "2          0.001708    0.051040    0.000325    0.054867    0.017870   \n",
              "3          0.000582    0.009326    0.000465    0.048315    0.023302   \n",
              "4          0.000207    0.023761    0.000747    0.019347    0.012749   \n",
              "\n",
              "prod_id  B00LED02VY  B00LGN7Y3G  B00LGQ6HL8  B00LI4ZZO8  B00LKG1MC8  \n",
              "0          0.016109    0.002855    0.174568    0.011367    0.012997  \n",
              "1          0.004251    0.002177    0.024362    0.014765    0.038570  \n",
              "2          0.004996    0.002426    0.083928    0.112205    0.005964  \n",
              "3          0.006790    0.003380    0.005460    0.015263    0.025996  \n",
              "4          0.001026    0.001364    0.020580    0.011828    0.012770  \n",
              "\n",
              "[5 rows x 48190 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-af282d94-6504-49b9-b705-91ac5e1fb05c\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th>prod_id</th>\n",
              "      <th>0594451647</th>\n",
              "      <th>0594481813</th>\n",
              "      <th>0970407998</th>\n",
              "      <th>0972683275</th>\n",
              "      <th>1400501466</th>\n",
              "      <th>1400501520</th>\n",
              "      <th>1400501776</th>\n",
              "      <th>1400532620</th>\n",
              "      <th>1400532655</th>\n",
              "      <th>140053271X</th>\n",
              "      <th>...</th>\n",
              "      <th>B00L5YZCCG</th>\n",
              "      <th>B00L8I6SFY</th>\n",
              "      <th>B00L8QCVL6</th>\n",
              "      <th>B00LA6T0LS</th>\n",
              "      <th>B00LBZ1Z7K</th>\n",
              "      <th>B00LED02VY</th>\n",
              "      <th>B00LGN7Y3G</th>\n",
              "      <th>B00LGQ6HL8</th>\n",
              "      <th>B00LI4ZZO8</th>\n",
              "      <th>B00LKG1MC8</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>0.005086</td>\n",
              "      <td>0.002178</td>\n",
              "      <td>0.003668</td>\n",
              "      <td>0.040843</td>\n",
              "      <td>0.009640</td>\n",
              "      <td>0.006808</td>\n",
              "      <td>0.020659</td>\n",
              "      <td>0.000649</td>\n",
              "      <td>0.020331</td>\n",
              "      <td>0.005633</td>\n",
              "      <td>...</td>\n",
              "      <td>0.000238</td>\n",
              "      <td>0.061477</td>\n",
              "      <td>0.001214</td>\n",
              "      <td>0.123433</td>\n",
              "      <td>0.028490</td>\n",
              "      <td>0.016109</td>\n",
              "      <td>0.002855</td>\n",
              "      <td>0.174568</td>\n",
              "      <td>0.011367</td>\n",
              "      <td>0.012997</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>0.002286</td>\n",
              "      <td>0.010898</td>\n",
              "      <td>0.000724</td>\n",
              "      <td>0.130259</td>\n",
              "      <td>0.007506</td>\n",
              "      <td>0.003350</td>\n",
              "      <td>0.063711</td>\n",
              "      <td>0.000674</td>\n",
              "      <td>0.016111</td>\n",
              "      <td>0.002433</td>\n",
              "      <td>...</td>\n",
              "      <td>0.000038</td>\n",
              "      <td>0.013766</td>\n",
              "      <td>0.001473</td>\n",
              "      <td>0.025588</td>\n",
              "      <td>0.042103</td>\n",
              "      <td>0.004251</td>\n",
              "      <td>0.002177</td>\n",
              "      <td>0.024362</td>\n",
              "      <td>0.014765</td>\n",
              "      <td>0.038570</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>0.001655</td>\n",
              "      <td>0.002675</td>\n",
              "      <td>0.007355</td>\n",
              "      <td>0.007264</td>\n",
              "      <td>0.005152</td>\n",
              "      <td>0.003986</td>\n",
              "      <td>0.003480</td>\n",
              "      <td>0.006961</td>\n",
              "      <td>0.006606</td>\n",
              "      <td>0.002719</td>\n",
              "      <td>...</td>\n",
              "      <td>0.001708</td>\n",
              "      <td>0.051040</td>\n",
              "      <td>0.000325</td>\n",
              "      <td>0.054867</td>\n",
              "      <td>0.017870</td>\n",
              "      <td>0.004996</td>\n",
              "      <td>0.002426</td>\n",
              "      <td>0.083928</td>\n",
              "      <td>0.112205</td>\n",
              "      <td>0.005964</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>0.001856</td>\n",
              "      <td>0.011019</td>\n",
              "      <td>0.005910</td>\n",
              "      <td>0.014134</td>\n",
              "      <td>0.000179</td>\n",
              "      <td>0.001877</td>\n",
              "      <td>0.005391</td>\n",
              "      <td>0.001709</td>\n",
              "      <td>0.004968</td>\n",
              "      <td>0.001402</td>\n",
              "      <td>...</td>\n",
              "      <td>0.000582</td>\n",
              "      <td>0.009326</td>\n",
              "      <td>0.000465</td>\n",
              "      <td>0.048315</td>\n",
              "      <td>0.023302</td>\n",
              "      <td>0.006790</td>\n",
              "      <td>0.003380</td>\n",
              "      <td>0.005460</td>\n",
              "      <td>0.015263</td>\n",
              "      <td>0.025996</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>0.001115</td>\n",
              "      <td>0.002670</td>\n",
              "      <td>0.011018</td>\n",
              "      <td>0.014434</td>\n",
              "      <td>0.010319</td>\n",
              "      <td>0.006002</td>\n",
              "      <td>0.017151</td>\n",
              "      <td>0.003726</td>\n",
              "      <td>0.001404</td>\n",
              "      <td>0.005645</td>\n",
              "      <td>...</td>\n",
              "      <td>0.000207</td>\n",
              "      <td>0.023761</td>\n",
              "      <td>0.000747</td>\n",
              "      <td>0.019347</td>\n",
              "      <td>0.012749</td>\n",
              "      <td>0.001026</td>\n",
              "      <td>0.001364</td>\n",
              "      <td>0.020580</td>\n",
              "      <td>0.011828</td>\n",
              "      <td>0.012770</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 48190 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-af282d94-6504-49b9-b705-91ac5e1fb05c')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-af282d94-6504-49b9-b705-91ac5e1fb05c button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-af282d94-6504-49b9-b705-91ac5e1fb05c');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 137
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "avg_preds=preds_df.mean()\n",
        "avg_preds.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "r19iVskYmTSV",
        "outputId": "d6a6540b-2d6f-4d9b-a27f-a2b783454a51"
      },
      "execution_count": 138,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "prod_id\n",
              "0594451647    0.003360\n",
              "0594481813    0.005729\n",
              "0970407998    0.008566\n",
              "0972683275    0.035330\n",
              "1400501466    0.006966\n",
              "dtype: float64"
            ]
          },
          "metadata": {},
          "execution_count": 138
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "rmse_df = pd.concat([average_rating, avg_preds], axis=1)\n",
        "\n",
        "rmse_df.columns = ['Avg_actual_ratings', 'Avg_predicted_ratings']\n",
        "\n",
        "rmse_df.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 237
        },
        "id": "5Aeap4h2mVTM",
        "outputId": "ccc881df-f14a-4d8c-fdb2-0e9efa7f9de7"
      },
      "execution_count": 139,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "            Avg_actual_ratings  Avg_predicted_ratings\n",
              "prod_id                                              \n",
              "0594451647            0.003247               0.003360\n",
              "0594481813            0.001948               0.005729\n",
              "0970407998            0.003247               0.008566\n",
              "0972683275            0.012338               0.035330\n",
              "1400501466            0.012987               0.006966"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-61a9cc92-e6ab-4a86-82af-75d306484123\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Avg_actual_ratings</th>\n",
              "      <th>Avg_predicted_ratings</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>prod_id</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0594451647</th>\n",
              "      <td>0.003247</td>\n",
              "      <td>0.003360</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0594481813</th>\n",
              "      <td>0.001948</td>\n",
              "      <td>0.005729</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0970407998</th>\n",
              "      <td>0.003247</td>\n",
              "      <td>0.008566</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0972683275</th>\n",
              "      <td>0.012338</td>\n",
              "      <td>0.035330</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1400501466</th>\n",
              "      <td>0.012987</td>\n",
              "      <td>0.006966</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-61a9cc92-e6ab-4a86-82af-75d306484123')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-61a9cc92-e6ab-4a86-82af-75d306484123 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-61a9cc92-e6ab-4a86-82af-75d306484123');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 139
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "RMSE=mean_squared_error(rmse_df['Avg_actual_ratings'], rmse_df['Avg_predicted_ratings'], squared=False)\n",
        "print(f'RMSE SVD Model = {RMSE} \\n')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "l9HPwqQwmWoq",
        "outputId": "e1c1c435-f583-4d1c-d34a-432366cef52f"
      },
      "execution_count": 141,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "RMSE SVD Model = 0.013679389779858 \n",
            "\n"
          ]
        }
      ]
    }
  ]
}