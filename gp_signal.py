import numpy as np
from sklearn.gaussian_process.kernels import ConstantKernel as kC, RBF as kRBF
from sklearn.gaussian_process.kernels import Kernel, NormalizedKernelMixin, Hyperparameter
from scipy.stats import f
from scipy.linalg import cholesky, solve_triangular, cho_solve
from sklearn.gaussian_process import GaussianProcessRegressor
import matplotlib.pyplot as plt
import warnings
from sklearn.utils.validation import check_array
class GPnew(GaussianProcessRegressor):
    def predict_new(self, X, return_std=False, return_cov=False, kx = None ):
        """Predict using the Gaussian process regression model
        We can also predict based on an unfitted model by using the GP prior.
        In addition to the mean of the predictive distribution, also its
        standard deviation (return_std=True) or covariance (return_cov=True).
        Note that at most one of the two can be requested.
        Parameters
        ----------
        X : sequence of length n_samples
            Query points where the GP is evaluated.
            Could either be array-like with shape = (n_samples, n_features)
            or a list of objects.
        return_std : bool, default: False
            If True, the standard-deviation of the predictive distribution at
            the query points is returned along with the mean.
        return_cov : bool, default: False
            If True, the covariance of the joint predictive distribution at
            the query points is returned along with the mean
        Returns
        -------
        y_mean : array, shape = (n_samples, [n_output_dims])
            Mean of predictive distribution a query points
        y_std : array, shape = (n_samples,), optional
            Standard deviation of predictive distribution at query points.
            Only returned when return_std is True.
        y_cov : array, shape = (n_samples, n_samples), optional
            Covariance of joint predictive distribution a query points.
            Only returned when return_cov is True.
        """
        if kx is None:
            kx_kern = self.kernel
            kx_kern_ = self.kernel_
        else:
            kx_kern = getattr(self.kernel, kx)
            kx_kern_ = getattr(self.kernel_, kx)
        
        if return_std and return_cov:
            raise RuntimeError(
                "Not returning standard deviation of predictions when "
                "returning full covariance.")

        if kx_kern is None or kx_kern.requires_vector_input:
            X = check_array(X, ensure_2d=True, dtype="numeric")
        else:
            X = check_array(X, ensure_2d=False, dtype=None)

        if not hasattr(self, "X_train_"):  # Unfitted;predict based on GP prior
            if kx_kern is None:
                kernel = (kC(1.0, constant_value_bounds="fixed") *
                          kRBF(1.0, length_scale_bounds="fixed"))
            else:
                kernel = kx_kern
            y_mean = np.zeros(X.shape[0])
            if return_cov:
                y_cov = kernel(X)
                return y_mean, y_cov
            elif return_std:
                y_var = kernel.diag(X)
                return y_mean, np.sqrt(y_var)
            else:
                return y_mean
        else:  # Predict based on GP posterior
            K_trans = kx_kern_(X, self.X_train_)
            y_mean = K_trans.dot(self.alpha_)  # Line 4 (y_mean = f_star)
            y_mean = self._y_train_mean + y_mean  # undo normal.
            
            if return_cov:
                v = cho_solve((self.L_, True), K_trans.T)  # Line 5
                y_cov = kx_kern_(X) - K_trans.dot(v)  # Line 6
                return y_mean, y_cov
            elif return_std:
                # cache result of K_inv computation
                # if self._K_inv is None:
                #     # compute inverse K_inv of K based on its Cholesky
                #     # decomposition L and its inverse L_inv
                #     L_inv = solve_triangular(self.L_.T,
                #                              np.eye(self.L_.shape[0]))
                #     self._K_inv = L_inv.dot(L_inv.T)
                L_inv = solve_triangular(self.L_.T, np.eye(self.L_.shape[0]))
                K_inv = L_inv.dot(L_inv.T)

                # Compute variance of predictive distribution
                y_var = kx_kern_.diag(X)
                y_var -= np.einsum("ij,ij->i",
                                   np.dot(K_trans, K_inv), K_trans)

                # Check if any of the variances is negative because of
                # numerical issues. If yes: set the variance to 0.
                y_var_negative = y_var < 0
                if np.any(y_var_negative):
                    warnings.warn("Predicted variances smaller than 0. "
                                  "Setting those variances to 0.")
                    y_var[y_var_negative] = 0.0
                return y_mean, np.sqrt(y_var)
            else:
                return y_mean

    def predict_partial(self, X, return_std=False, return_cov=False, kx=None):
        return self.predict_new(X, return_std, return_cov, kx)
    
    def get_dof(self,X,kx = None):
        kx_kern_ = self.kernel_
        if kx is not None:
            for kn in kx.split('.'):
                kx_kern_ = getattr(kx_kern_, kn)
        K_trans = kx_kern_(X, self.X_train_)
        L_inv = solve_triangular(self.L_.T, np.eye(self.L_.shape[0]))
        self._K_inv_ = L_inv.dot(L_inv.T)
#         print(self._K_inv_)
        return K_trans, np.trace(np.matmul(K_trans, self._K_inv_))

    def get_dof2(self,X,dy):
        kx_kern_ = self.kernel_
        kx = None
        if kx is not None:
            for kn in kx.split('.'):
                kx_kern_ = getattr(kx_kern_, kn)
        K_trans = kx_kern_(X, self.X_train_)
        L_inv = solve_triangular(self.L_.T, np.eye(self.L_.shape[0]))
        self._K_inv_ = L_inv.dot(L_inv.T)
        Mat = np.matmul(K_trans, self._K_inv_)
        mat2 = np.copy(Mat)
        for i in range(Mat.shape[0]):
            for j in range(Mat.shape[1]):
                mat2[i,j] = Mat[i,j]*(dy[j]/dy[i])
#                 print(Mat[i,j],dy[j],dy[i],Mat[i,j]*(dy[j]/dy[i]),mat2[i,j])
#                 print(Mat[i,j],mat2[i,j])
#         print(np.max(Mat),np.max(mat2),np.max(np.abs(Mat-mat2)))
#         print(np.trace(Mat), np.trace(mat2), np.trace(np.matmul(mat2,np.transpose(mat2))), np.trace(2*mat2 - np.matmul(mat2,np.transpose(mat2))))
        return np.trace(Mat), np.trace(mat2), np.trace(np.matmul(mat2,np.transpose(mat2))), np.trace(2*mat2 - np.matmul(mat2,np.transpose(mat2))),Mat,mat2

from sklearn.gaussian_process.kernels import Kernel, Hyperparameter 
class Signal( Kernel):
    def __init__(self, mass = 1e-5, mass_bounds = (1e-5, 1e5) , width = 1e-5, width_bounds = (1e-5, 1e5)):
        self.mass = mass
        self.mass_bounds = mass_bounds
        self.width = width
        self.width_bounds = width_bounds # lower bound on width must be greater than or equal to 1
        
    @property
    def hyperparameter_mass(self):
        return Hyperparameter("mass", "numeric", self.mass_bounds)
    
    @property
    def hyperparameter_width(self):
        return Hyperparameter("width", "numeric", self.width_bounds)
        
    def __call__(self, X, Y=None, eval_gradient=False):
        X = np.atleast_2d(X)
#         factor = 1#/np.sqrt(np.pi*2)
        if Y is None:  
            K = np.exp(-0.5* ( np.square(X - self.mass)+ np.square(X.reshape(-1) - self.mass)) / np.square(self.width))  
        else:
            if eval_gradient:
                raise ValueError("Gradient can only be evaluated when Y is None.")
            K = np.exp(-0.5* ( np.square(X - self.mass) + np.square(Y.reshape(-1) - self.mass)) / np.square(self.width))  
            
            
        if eval_gradient:
            if not self.hyperparameter_mass.fixed:
                mass_gradient = K * self.mass * ( X + X.reshape(-1)- 2*self.mass) / np.square(self.width)
                mass_gradient = mass_gradient[:, :, np.newaxis]
            else: # mass is kept fixed
                mass_gradient = np.empty((K.shape[0], K.shape[1], 0))

            if not self.hyperparameter_width.fixed:
                width_gradient = K*(np.square(X - self.mass) + np.square(X.reshape(-1)-self.mass))/ np.square(self.width)
                width_gradient = width_gradient[:, :, np.newaxis]
            else: # width is kept fixed
                width_gradient = np.empty((K.shape[0], K.shape[1], 0))
  
            return K, np.dstack((mass_gradient, width_gradient))
        else:
            return K
        
    def is_stationary(self):
        return False
        
    def __repr__(self):
        return "{0}(mass={1:.3g}, width={2:.3g})".format(self.__class__.__name__, self.mass, self.width)
    
    def diag(self, X):
        # factor = 1 #/np.sqrt(np.pi*2)
#         K = factor*np.exp(-0.5* ( np.square(X - self.mass)+ np.square(X.reshape(-1) - self.mass)) / np.square(self.width))  
#         return np.diag(K)
        return np.exp(- np.square ((X.reshape(-1) - self.mass)  / self.width) )  
