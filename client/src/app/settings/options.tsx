import { useRouter } from 'next/navigation'

const Options: React.FC = () => {
    const router = useRouter();

    return (
        <div className="flex min-h-screen bg-slate-900 text-gray-100">
            <div className="p-6">
          <h2 className="text-xl font-semibold mb-6 text-gray-200">Options</h2>
          <div className="grid gap-4 max-w-md">
            <button className="flex items-center gap-4 bg-slate-800 hover:bg-slate-700 p-4 rounded-lg transition-colors border border-slate-700 text-left">
              <div className="p-2 bg-blue-500 bg-opacity-20 rounded-lg">👤</div>
              <span className="font-medium">Profile Settings</span>
            </button>
            
            <button className="flex items-center gap-4 bg-slate-800 hover:bg-slate-700 p-4 rounded-lg transition-colors border border-slate-700 text-left">
              <div className="p-2 bg-purple-500 bg-opacity-20 rounded-lg">❓
              </div>
              <span className="font-medium">Application Support</span>
            </button>
            
            <button className="flex items-center gap-4 bg-slate-800 hover:bg-slate-700 p-4 rounded-lg transition-colors border border-slate-700 text-left" onClick={() => router.push('/')}>
              <div className="p-2 bg-red-500 bg-opacity-20 rounded-lg"> ➡️
              </div>
              <span className="font-medium">Log Out</span>
            </button>
          </div>
        </div>
        </div>
    );
    
};

export default Options;
