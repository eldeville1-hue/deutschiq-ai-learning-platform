import React from 'react';
import { FaArrowRight, FaExclamationTriangle, FaRoute } from 'react-icons/fa';

type ProductStateProps = {
  eyebrow: string;
  title: string;
  detail: string;
  action: string;
  onAction: () => void;
  kind?: 'empty' | 'error';
};

export const ProductState: React.FC<ProductStateProps> = ({
  eyebrow,
  title,
  detail,
  action,
  onAction,
  kind = 'empty',
}) => (
  <section className={`dq-product-state ${kind}`} role={kind === 'error' ? 'alert' : 'status'}>
    <span className="dq-product-state-icon" aria-hidden="true">
      {kind === 'error' ? <FaExclamationTriangle /> : <FaRoute />}
    </span>
    <div>
      <small>{eyebrow}</small>
      <h2>{title}</h2>
      <p>{detail}</p>
    </div>
    <button type="button" onClick={onAction}>
      <span>{action}</span><FaArrowRight />
    </button>
  </section>
);
