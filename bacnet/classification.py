class BacnetClassificationResult:
    predicted_class = ""
    score = 0.0

    def __init__(self, predicted_class: str, score: float):
        self.predicted_class = predicted_class
        self.score = score

    def __str__(self):
        return "("+self.predicted_class+","+str(self.score)+")"

class BacnetClassification:
    '''
    Performs device_classification on bacnet test_devices based on text retrieved from object queries, which is provided as input.
    '''

    def __init__(self, classification_threshold: float, scraping_threshold: float):
        from device_classification.text_classification import DeviceClassifier
        from web_scraping.scraping import RelevantTextScraper
        self.threshold = classification_threshold
        self.text_scraper = RelevantTextScraper(scraping_threshold)
        self.classifier = DeviceClassifier(threshold=classification_threshold)

    def classify_bacnet_objects(self, queried_objects: str) -> BacnetClassificationResult:
        '''
        Takes the queried objects of a device as input, cleans the input and preforms device_classification.
        :param queried_objects: The queried objects of the device in json format
        :return: BacnetClassificationResult containing predicted class and score.
        '''
        from web_scraping.google import GoogleCustomSearchAPI
        from bacnet.utilities import BacnetUtilities
        from web_scraping.bing import BingSearchAPI
        import operator

        '''
        Preparing classification based on search engines.
        '''
        search_terms = ""

        deviceType = BacnetUtilities.get_deviceType_from_query(queried_objects)
        description = BacnetUtilities.get_description_from_query(queried_objects)

        if deviceType != "":
            search_terms = deviceType
        elif description != "":
            search_terms = description
        else:
            vendor_name = BacnetUtilities.get_vendor_name_from_query(queried_objects)
            model_name = BacnetUtilities.get_model_name_from_query(queried_objects)
            device_object_name = BacnetUtilities.get_device_object_name_from_query(queried_objects) #Not useful?

            search_terms = vendor_name + " " + model_name# + " " + device_object_name

        print("Search terms: " + search_terms)

        '''
        Classification based on Bing and Google
        '''

        print("Classifying using Bing and Google...")

        urls = BingSearchAPI.first_ten_results(search_terms,only_html=False)+GoogleCustomSearchAPI.search(search_terms,exclude_pdf=False)

        cumulative_scores = self.text_scraper.cumulative_classification(set(urls),r2_scoring=True)

        if len(cumulative_scores) > 0:
            best_classification = max(cumulative_scores)
            best_classification_score = max(cumulative_scores.values())
        else:
            best_classification = ""
            best_classification_score = 0.0

        if best_classification_score > self.threshold and best_classification is not "":
            return BacnetClassificationResult(best_classification,best_classification_score)
        else:
            print("Failed...")
            return BacnetClassificationResult("No_classification",0.0)


if __name__ == "__main__":
    from bacnet.local_device_applications.test_devices import arob,bacdrpc,bacri,bacrpc,bacsri,cdd3,cdrbac,src100,touchplateultra
    from web_scraping.scraping import RelevantTextScraper
    from bacnet.utilities import BacnetUtilities

    text = arob.run_application()

    bc = BacnetClassification(0.2,0.1)

    print(bc.classify_bacnet_objects(text))


