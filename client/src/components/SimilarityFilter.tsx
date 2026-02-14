interface Props {
  value: number;
  onChange: (v: number) => void;
}

export default function SimilarityFilter({ value, onChange }: Props) {
  const getFilterLabel = (val: number) => {
    if (val >= 0.8) return "Very High";
    if (val >= 0.6) return "High";
    if (val >= 0.4) return "Medium";
    if (val >= 0.2) return "Low";
    return "All";
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium text-gray-700">
          Minimum Similarity
        </label>
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold text-blue-600">
            {(value * 100).toFixed(0)}%
          </span>
          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
            {getFilterLabel(value)}
          </span>
        </div>
      </div>
      
      <div className="relative">
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600 hover:accent-blue-700"
          style={{
            background: `linear-gradient(to right, #2563eb 0%, #2563eb ${value * 100}%, #e5e7eb ${value * 100}%, #e5e7eb 100%)`
          }}
        />
        
        {/* Tick marks */}
        <div className="flex justify-between mt-1 px-1">
          {[0, 0.25, 0.5, 0.75, 1].map((tick) => (
            <button
              key={tick}
              onClick={() => onChange(tick)}
              className="text-xs text-gray-400 hover:text-gray-600 transition-colors"
            >
              {(tick * 100).toFixed(0)}%
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}