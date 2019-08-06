import pandas
import Structure
import Attribute
import Naive_Bayes_Classifier


class Model:
    def __init__(self, filename, structure, binsNum):
        self.structure = structure
        self.columns = {}
        self.columnNames = []
        self.numberOfRows = None
        self.build_model(filename, binsNum)

    def build_model(self, filename,binsNum):
        columns = []
        for att in self.structure.attributes:
            columns.append(att.name)
        columns.append(self.structure.classAttribute.name)

        self.columnNames = columns

        data = pandas.read_csv(filename, names=columns)
        header = data.iloc[0,:].tolist()
        if header != columns:
            raise Exception("The attributes in file: '" + str(filename) + "', must consist to the structure file.")
        data.fillna(data.mean())
        for i in range(len(columns)):
            if i == len(columns) - 1:
                currAttribute = self.structure.classAttribute
            else:
                currAttribute = self.structure.attributes[i]
            colDataFrame = data.iloc[1:,i]
            if isinstance(currAttribute, Attribute.Numeric):
                colDataFrame = colDataFrame.apply(pandas.to_numeric)
                colDataFrame = colDataFrame.fillna(colDataFrame.mean())
                col_min = colDataFrame.min()
                col_max = colDataFrame.max()
                col_bin_step = (col_max - col_min) / binsNum
                currAttribute.set_bins_data(col_min, col_max, col_bin_step)

                col = colDataFrame.tolist()

                for j in range(len(col)):
                    col[j] = currAttribute.get_bin_number(col[j])

            elif isinstance(currAttribute, Attribute.Category):
                colDataFrame = colDataFrame.fillna(colDataFrame.max())
                col = colDataFrame.tolist()
            else:
                raise Exception("This is just weird...")

            self.columns[currAttribute.name] = col
        self.numberOfRows = len(self.columns[self.structure.classAttribute.name])
        self.train()

    def train(self):
        for attribute in self.structure.attributes:
            for value in attribute.categories:
                value.setAppNum(self.columns[attribute.name].count(value.name))
                details = {}
                for classification in self.structure.classAttribute.categories:
                    counter = 0
                    for i in range(len(self.columns[attribute.name])):
                        if(self.columns[attribute.name][i] == value.name and self.columns[self.structure.classAttribute.name][i] == classification.name):
                            counter += 1
                    details[classification.name] = counter
                value.addClassQuantity(details)
        for classification in self.structure.classAttribute.categories:
            classification.setAppNum(self.columns[self.structure.classAttribute.name].count(classification.name))

    def classify(self, test_filename, outputPath):
        with open(outputPath, mode='w') as out_file:
            record_num = 1
            lines = [line.rstrip('\n') for line in open(test_filename)]  # read all lines from test file
            line_count = 0
            for line in lines:
                row = line.split(',')
                if len(row) != len(self.structure.attributes) + 1:
                    raise Exception("The attributes in file: '" + str(test_filename) + "', must consist to the structure file. (Error in line number " + str(line_count) + ")")
                if line_count == 0:
                    self.checkFirstRow(row,test_filename)
                else:
                    if "" in row:
                        classification = "Bad input!"
                    else:
                        classification = self.getClassification(row)
                    out_file.write(str(record_num) + " " + classification + "\n")
                    record_num += 1
                line_count += 1

    def getClassification(self, details):
        realDetails = []
        results = {}
        for classification in self.structure.classAttribute.categories:
            results[classification.name] = float(classification.appNum)/self.numberOfRows
        for i in range(len(details)-1):
            if isinstance(self.structure.attributes[i], Attribute.Numeric):
                details[i] = self.structure.attributes[i].get_bin_number(float(details[i]))
            for value in self.structure.attributes[i].categories:
                if value.name == details[i]:
                    realDetails.append(value)
        for i in range(len(realDetails) - 1):
            value = realDetails[i]
            for classification in self.structure.classAttribute.categories:
                nc = value.classQuantity[classification.name]
                p = float(1) / len(self.structure.attributes[i].categories)
                n = value.appNum
                grade = Naive_Bayes_Classifier.calculateMestimate(p,nc,n)
                results[classification.name] *= grade
        max = 0
        classMax = None
        for classification in self.structure.classAttribute.categories:
            if results[classification.name] > max:
                classMax = classification.name
                max = results[classification.name]
        return "P(Y) = " + str(results['Y']) + " , P(N) = " + str(results['N']) + " ==> class = " + str(classMax)
        #return classMax

    def checkFirstRow(self, row,filename):
        # check the attributes line:
        for i in range(len(row)):
            if i == len(row) - 1:
                if str(row[i]) != str(self.structure.classAttribute.name):
                    raise Exception("The attribute: '" + str(row[i]) + "' in file: '" + str(
                        filename) + "', is expected to be named: '" + str(
                        self.structure.classAttribute.name) + "', as mentioned in the structure file")
            else:
                if str(row[i]) != str(self.structure.attributes[i].name):
                    raise Exception("The attribute: '" + str(row[i]) + "' in file: '" + str(
                        filename) + "', is expected to be named: '" + str(
                        self.structure.attributes[i].name) + "', as mentioned in the structure file")
