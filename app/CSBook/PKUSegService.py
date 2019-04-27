
import pkuseg

'''
    尝试一下北大开源的一款中文分词包—PKUSeg
    github地址：https://github.com/lancopku/pkuseg-python.git
    pkuseg.pkuseg(model_name = "default", user_dict = "default", postag = False)
	model_name :模型路径。
        "default"，默认参数，表示使用我们预训练好的混合领域模型(仅对pip下载的用户)。
        "news", 使用新闻领域模型。
        "web", 使用网络领域模型。
        "medicine", 使用医药领域模型。
        "tourism", 使用旅游领域模型。
	    model_path, 从用户指定路径加载模型。
	user_dict:设置用户词典。
        "default", 默认参数，使用我们提供的词典。
        None, 不使用词典。
        dict_path, 在使用默认词典的同时会额外使用用户自定义词典，可以填自己的用户词典的路径，词典格式为一行一个词。
	postag:是否进行词性分析。
        False, 默认参数，只进行分词，不进行词性标注。
        True, 会在分词的同时进行词性标注。
'''
trainFile = 'D:/book_infor/bookinfor.txt' #训练文件路径
testFile = 'D:/book_infor/data/test.txt' #测试文件路径
savedir = 'D:/book_infor/data/savedir/features.pkl' #训练模型的保存路径
#pkuseg.pkuseg(model_name='web',user_dict='default',postag=True)
#pkuseg.train(trainFile, testFile, savedir, train_iter = 20, init_model = None)


def wordCut():
    file = open(trainFile,'r',encoding='UTF-8')
    seg = pkuseg.pkuseg(user_dict=savedir)
    for line in file.readlines():
        words =  seg.cut(line)
        print(words)