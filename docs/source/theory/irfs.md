# Impulse Response Functions (IRFs)

The radiation force in the time-domain can be obtained by convolution:

$$
\begin{equation}
  \vec{f}_{rad}(t) = \mathbf{K}_{rad}(t) * \dot{\vec{s}}(t) = \int^t_{-\infty}\mathbf{K_{rad}}(t-\tau) \dot{\vec{s}}(\tau)d\tau
\end{equation}
$$

Where the radiation IRF (RIRF) can be obtained by cosine transformation:

$$
\begin{equation}
  \mathbf{K}_{rad}(t) = \frac{2}{\pi}\int^{\infty}_0\mathbf{B}(\omega) cos(\omega t) d\omega 
\end{equation}
$$