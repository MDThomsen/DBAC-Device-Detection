if __name__ == "__main__":
    from Dataset_Creation.DataSetCreator import DataSetCreator
    import os

    ds_creator = DataSetCreator(os.path.join(os.path.join(os.getcwd(),"data"),"dataset_urls.txt"))
    ds_creator.create_local_data_set(os.path.join(os.path.join(os.getcwd(),"data"),"dataset"))


