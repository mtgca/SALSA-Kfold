import pandas as pd

rooms = [1, 2]

perms = {1: [[2, 3, 4, 5], [1]],
         2: [[1, 3, 4, 5], [2]],
         3: [[1, 2, 4, 5], [3]],
         4: [[1, 2, 3, 5], [4]],
         5: [[1, 2, 3, 4], [5]]} # {key: permutation_number, value: [[train_splits], [validation_splits]]}

#string constructor
def make_string(fold, room, mix):
    '''Generate string for file name
    fold = fold number
    room = room number
    mix = mix number
    '''
    if mix%10 == mix:
        return "fold" + str(fold) + "_room" + str(room) + "_mix00" + str(mix)
    else:
        return "fold" + str(fold) + "_room" + str(room) + "_mix0" + str(mix)

#Generate fold names
def fold_generator(val_split, perms=perms):
    '''
    Generate fold names
    i.e. fold1_room1_mix001
    '''
    train_folds_names = [make_string(fold, room, mix) for fold in perms[val_split][0] for room in rooms for mix in range(1, 51)]
    val_folds_names = [make_string(val_split, room, mix) for room in rooms for mix in range(1, 51)]
    
    return train_folds_names, val_folds_names

# Create .csv files for each fold
def make_csv(val_split, fold_names, path="./dataset/meta/dcase2021/original/"):
    '''Generate .csv files for each fold, training and validation'''
    train_df = pd.DataFrame(fold_names[0], columns=["filename"])
    train_df.to_csv(path + "train_perm" + str(val_split) + ".csv", index=False)

    val_df = pd.DataFrame(fold_names[1], columns=["filename"])
    val_df.to_csv(path + "val_perm" + str(val_split) + ".csv", index=False)


if __name__ == "__main__":
    for val_perm in perms.keys():
        fold_names = fold_generator(val_perm)
        make_csv(val_perm, fold_names)


