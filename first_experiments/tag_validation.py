import pandas as pd

STATE_df = pd.read_pickle('STATE_val_df.pkl')

sense_labels = []
count = 1

for row in STATE_df.iterrows():
	print(count, row[1]['sentences'])
	print("1: condition\n2: political\n3: declare")
	label = input("Pleaase identify the appropriate word sense: ")
	sense_labels.append(label)
	count+=1
	#row[1]['sense_labels'] = int(label)

STATE_df['sense_labels'] = sense_labels

STATE_df.to_pickle('STATE_val_df_labeled')
