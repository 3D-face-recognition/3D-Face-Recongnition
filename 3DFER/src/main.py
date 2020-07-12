from src.file_process import FileProcess

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.decomposition import PCA
import  numpy as np
import matplotlib.pyplot as plt
#
fp = FileProcess()
X, y = fp.load_file()
# print("X:\n", X)
# X = [[1, 2, 3], [2, 4, 5, 6], [12, 3,4, 1, 3, 2, 31], [1, 1, 1, 1, 3]]
# y = [0, 0, 1, 1]
# def complement_X_missing(X, y):
#     X_copy = X.copy()
#     X_new = []
#
#     while(True):
#         print(len(X_copy))
#         x_len = [len(x) for x in X_copy]
#         x_max_length_index = np.argmax(x_len)
#         max_length = x_len[x_max_length_index]
#         most_freq = np.argmax(np.bincount(x_len))
#         print("max len of x: %s, most freq len of x: %s"%(max_length, most_freq))
#         if max_length > most_freq + 1:
#             X_copy = np.delete(X_copy, x_max_length_index)
#             y = np.delete(y, x_max_length_index)
#         else:
#             break
#     # complement zeros
#     for x in X_copy:
#         x = [x[i] if i < len(x) else 0 for i in range(max_length)]
#         X_new.append(x)
#     print("len(X_new): %s, len(y): %s" % (len(X_new), len(y)))
#     return  np.array(X_new), np.array(y)

for x in X:
    print(len(x))
# X, y = complement_X_missing(X, y)
std = StandardScaler()
X_std = std.fit_transform(X)

# fit model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

std = StandardScaler()
X_train_std = std.fit_transform(X_train)
X_test_std = std.transform(X_test)

pca = PCA(n_components=10)
X_train_pca = pca.fit_transform(X_train_std)
X_test_pca = pca.transform(X_test_std)
svc = SVC(gamma='auto')
svc.fit(X_train_pca, y_train)

print("training data accuracy:", svc.score(X_train_pca, y_train))
print("testing data accuracy: ", svc.score(X_test_pca, y_test))

fig = plt.figure()
plt.subplots(121)
for hog in X_std[y==0]:
    plt.plot([i for i in range(len(hog))], hog)
plt.title("angry")
plt.ylabel("value of hog")

plt.subplots(122)
for hog in X_std[y==3]:
    plt.plot([i for i in range(len(hog))], hog)
plt.title("happy")
plt.ylabel("value of hog")
plt.show()
# # visualize V0 and V3, they mean coordination of K0 and K0.
# X_happy_x = []
# X_happy_y = []
# for i in range(len(X_train_pca[y_train == 3])):
#     X_happy_x.append(X_train_pca[y_train == 3][i][0])
#     X_happy_y.append(X_train_pca[y_train == 3][i][1])
#
# X_angry_x = []
# X_angry_y = []
# for i in range(len(X_train_pca[y_train == 0])):
#     X_angry_x.append(X_train_pca[y_train == 0][i][0])
#     X_angry_y.append(X_train_pca[y_train == 0][i][1])
#
# # #plot image
# # visualize V0 and V1, v0 and v1 mean coordination of x,y
# fig = plt.figure(figsize=(18, 9))
# plt.subplot(1, 2, 1)
# plt.scatter(X_happy_x, X_happy_y, label="Angry", alpha=0.5)
# plt.scatter(X_angry_x, X_angry_y,label="Happy", alpha=0.5)
# plt.title("The scatter of v0, v1")
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.legend()
# plt.show()