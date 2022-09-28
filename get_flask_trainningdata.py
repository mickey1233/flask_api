import glob
import os
import requests

class GetTrainningData:
    def __init__(self,url):
        self.trainning_data_list = []
        self.url = url
        #self.file_path = glob.glob(os.path.join(path,'*','*.dgp'))
        #print(self.file_path)
        response = requests.get('{}/files'.format(url))
        response = response.json()
        for i in response[1]:
            r = requests.get('{}/dir/{}'.format(url,i))
            for j in r.json():
                image_pixel = []
                label = i
                r1 = requests.get('{}/download/{}/{}'.format(url,i,j))
                image_pixel = [0 if y == '0' else 1 for j in r1.text for y in j if y == '0' or y == '1' ]
                self.trainning_data_list.append([image_pixel,label])
            
    def __getitem__(self,index1):
        return self.trainning_data_list[index1]
    
    def __len__(self):
        return len(self.trainning_data_list)
         
    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        if self.index < len(self.trainning_data_list)-1:
            self.index += 1
            return self.trainning_data_list[self.index]
        else:
            raise StopIteration

if __name__ == '__main__':
    get_data = GetTrainningData('http://127.0.0.1:5000')
    
    for data in get_data:
        print(data)
        
            
            