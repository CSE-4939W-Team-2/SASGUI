import React from 'react';

const Slider = ({ label, value, onChange }) => {
    return (
        <div>
            <label>{label}</label>
            <input
                type="range"
                min="0"
                max="10"
                step="0.1"
                value={value}
                onChange={(e) => onChange(parseFloat(e.target.value))}
            />
            <span>{value}</span>
        </div>
    );
};

export default Slider;
