Architectures.csv:

Each row represents a model's architecture, and the layers added to the model are built sequentially from left to right. Build options implemented are as follows:


[0]: Initial Dense Layer: Dense layer configured with the input_size argument. Suitable only for first layer.

[1]: Dense Layer: Standard dense layer for use anywhere in the model except for the final position.

[2]: Final Dense Layer: Standard dense layer with units set to 1 for regression output. For use only as the final layer in a model.

[3]: Initial Solo LSTM Layer: LSTM layer configured with the input_size argument and no return_sequences. Suitable only for first layer.

[4]: Solo LSTM Layer: LSTM layer for use without a following LSTM. Can be placed anywhere within a model, just not first or last layer.

[5]: Initial Multi LSTM Layer: LSTM layer configured with the input_size argument and return_sequences. Suitable only for first layer.

[6]: Multi LSTM Layer: LSTM layer for use with subsequent LSTM layers. Can be used anywhere except the final position in the model.

[7]: Final LSTM Layer: LSTM layer configured to serve as the final layer in a model. 

[8]: Time Distributed Dense Layer: For use as final layer in the model.


Build Options.csv:

Options are categorized by row, details given below:

Row 1-8: Build Options (Associated with different architecture layers as shown above)
---Col A: Use bias setting (Boolean)
---Col B: Activation function (String) 
---Col C: Unused, reserved
---Col D: Bias initializer function (String)

Options.csv

Each row is a different option set as described below:

Row 1: Compile Options
---Col A: Optimizer 		(Default is adam)
---Col B: Loss Function 	(Regression, so default is mse)
Row 2: Train Options
---Col A: Epochs setting
---Col B: Verbose setting 	(Default 2)
---Col C: Initial epoch set 	(Default 0)
---Col D: Max queue size 	(Default 10)
Row 3: Eval Options
---Col A: Verbose setting 	(Default 1)
Row 4: Data Import Options
---Col A: Batch count 		(Default 25)
---Col B: Sample Rate 		(Default 1)
---Col C: Stride Length 	(Default 1)