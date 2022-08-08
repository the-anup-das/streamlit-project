import streamlit as st
from sklearn import datasets

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

import numpy as np

st.title("Best Classifier")
st.write("""
    # Explore streamlit classifiers
    which one is the best?
""")

datagroup_name = st.sidebar.selectbox("Select Dataset", ("Iris","Breast Cancer","Wine dataset"))
# st.write(datagroup_name)

classifiergroup_name = st.sidebar.selectbox(
    "Select Classifier",("KNN","SVM","Random Forest", "Decision Tree")
)

def pick_dataset(datagroup_name):
    if datagroup_name == "Iris":
        data = datasets.load_iris()
    elif datagroup_name == "Breast Cancer":
        data = datasets.load_breast_cancer()
    else:
        data = datasets.load_wine()

    X = data.data
    y = data.target

    return X,y

X,y = pick_dataset(datagroup_name)
st.write("shape of dataset", X.shape)
st.write("Number of classes", len(np.unique(y)))

def put_parameter_ui(clfs_name):
    params = dict()
    if clfs_name == "KNN":
        K = st.sidebar.slider("K", 1, 14)
        params["K"] = K
        
    elif clfs_name == "SVM":
        S = st.sidebar.slider("C",0.03,9.0)
        params["S"] = S
    else:
        max_depth_val = st.sidebar.slider("max_depth_val",1,13)
        n_estimate = st.sidebar.slider("n_estimate",1,100)
        params["max_depth_val"] = max_depth_val
        params["n_estimate"] = n_estimate
    
    return params


params = put_parameter_ui(classifiergroup_name)

def have_classifier(clfs_name, params):
    if clfs_name == "KNN":
        clf = KNeighborsClassifier(n_neighbors = params["K"])
    elif clfs_name == "SVM":
        clf = SVC(C = params["S"])
    else:
        clf = RandomForestClassifier(n_estimators = params["n_estimate"],
                                max_depth = params["max_depth_val"],
                                random_state=100
        )

    return clf

clf = have_classifier(classifiergroup_name, params)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state = 100)

clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
ac = accuracy_score(y_test, y_pred)

st.write(f"Classifier = {classifiergroup_name}")
st.write(f"accuracy = {ac}")

#plot

pca = PCA(2)

X_projection = pca.fit_transform(X)

x1 = X_projection[:, 0]
x2 = X_projection[:, 1]

fig, ax = plt.subplots(figsize = (10,5))

ax.set_prop_cycle(color=['red', 'green', 'blue'])
ax.scatter(x1, x2, c=y, alpha=0.8, cmap="viridis")
ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 1")

# fig.colorbar(ax)

st.pyplot(fig)