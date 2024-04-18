import Image from 'next/image';
import Link from 'next/link';

export default function Home() {
  return (
    <>
      <nav className="fixed top-0 z-10 w-full bg-white shadow">
        <div className="container mx-auto px-4 py-2 flex justify-end items-center">
          <Link href="https://github.com/wweggplant/holiday-calendar-remind-sub" aria-label="GitHub Project" className="text-gray-500 hover:text-gray-600">
            <Image src="/github-mark.svg" alt="GitHub Logo" width={32} height={32} />
          </Link>
        </div>
      </nav>
      <div className="pt-16 flex flex-col items-center justify-center bg-blue-50 min-h-screen px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-700 mb-2">
            火车票预约 | 一“键”掌握
          </h1>
          <p className="mb-4 text-sm sm:text-base text-gray-500">
            导入日历，提醒节假日前后和调休当天预订火车票
          </p>
          <Link href='/bookTrain.ics' className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition-colors duration-150 ease-in-out">
            点击导入日历
          </Link>
          <div className="mt-10 w-full max-w-100 overflow-x-auto whitespace-nowrap overflow-x-visible flex justify-center items-center">
            <div className="inline-block w-auto sm:flex-shrink-0 relative sm:max-w-[300px]">
              <Image alt="示例图1" layout='responsive' width={292.5} height={633} src={'/p1.png'} priority />
            </div>
            <div className="inline-block w-auto sm:flex-shrink-0 relative sm:max-w-[300px] ml-1">
              <Image alt="示例图2" layout='responsive' width={292.5} height={633} src={'/p2.png'} priority />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
