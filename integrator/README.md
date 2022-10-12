See a explanation of the columns in a table, as documented in [setup.py](setup.py#L33).

![An image showing a explanation of the table columns](../docs/table-demo.gif)

The below animation illustrates how a completed table is being converted into a list.

![An animation showing an example of what the integrator does](../docs/integrator-demo.gif) 

This image shows how the index differs from the list.

![An image showing an example of what the index generator does](../docs/indexgenerator-demo.gif) [src](https://docs.google.com/presentation/d/1QJGfndGEz3s0MTzaVZ7T3PywzJ_DmIANtfSbkfgmQBs)

See futher examples for both in [test](test/)

The range of sources are provided in [`sl-sources.txt`](https://github.com/mapto/UchitelnoEvangelie/blob/master/integrator/sl-sources.txt) and [`gr-sources.txt`](https://github.com/mapto/UchitelnoEvangelie/blob/master/integrator/gr-sources.txt). The first line in each contains the main manuscript reference. For the way how default (implicit) variant source is indicated, see implementation in [`config.py`](https://github.com/mapto/UchitelnoEvangelie/blob/master/integrator/config.py), lines [`DEFAULT_SL: str = "".join(VAR_SL)`](https://github.com/mapto/UchitelnoEvangelie/blob/master/integrator/config.py#L52) and [`DEFAULT_GR: str = VAR_GR[0]`](https://github.com/mapto/UchitelnoEvangelie/blob/master/integrator/config.py#L54).
